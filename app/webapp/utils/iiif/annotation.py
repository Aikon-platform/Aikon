import json
import re
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen

import requests
from PIL import Image

from app.webapp.models.regions import Regions, get_name
from app.webapp.models.digitization import Digitization
from app.webapp.models.treatment import Treatment
from app.webapp.utils.constants import MANIFEST_V2, MANIFEST_V1
from app.config.settings import (
    CANTALOUPE_APP_URL,
    SAS_APP_URL,
    APP_NAME,
    APP_URL,
)
from app.webapp.utils.functions import log, get_img_nb_len
from app.webapp.utils.iiif import parse_ref, gen_iiif_url, region_title
from app.webapp.utils.paths import REGIONS_PATH, IMG_PATH
from app.webapp.utils.regions import get_txt_regions

IIIF_CONTEXT = "http://iiif.io/api/presentation/2/context.json"


def index_regions(regions: Regions):
    if not index_manifest_in_sas(regions.gen_manifest_url(version=MANIFEST_V2), True):
        return

    canvases_to_annotate = get_annotations_per_canvas(regions)
    if not bool(canvases_to_annotate):
        # if the annotation file is empty
        return True

    for c in canvases_to_annotate:
        try:
            index_annotations_on_canvas(regions, c)
        except Exception as e:
            log(
                f"[index_regions] Problem indexing region #{regions.id} (canvas {c})",
                e,
            )

    return True


def get_regions_annotations(
    regions: Regions, as_json=False, r_annos=None, min_c: int = None, max_c: int = None
):
    if r_annos is None:
        r_annos = {} if as_json else []

    region_ref = regions.get_ref()
    try:
        r = requests.get(f"{SAS_APP_URL}/search-api/{region_ref}/search")
        annos = r.json()["resources"]
    except Exception as e:
        log(
            f"[get_regions_annotations]: Failed to get annotations in SAS for Regions #{regions.id}",
            e,
        )
        return r_annos

    img_name = region_ref.split("_anno")[0]
    nb_len = get_img_nb_len(img_name)

    for anno in annos:
        try:
            canvas = anno["on"].split("/canvas/c")[1].split(".json")[0]
            xyhw = anno["on"].split("xywh=")[1]
            if min_c is not None and (int(canvas) < min_c or int(canvas) > max_c):
                continue
            if as_json:
                if canvas not in r_annos:
                    r_annos[canvas] = {}
                img = f"{img_name}_{canvas.zfill(nb_len)}"
                aid = anno["@id"].split("/")[-1]
                r_annos[canvas][aid] = {
                    "id": aid,
                    "ref": f"{img}_{xyhw}",
                    "class": "Region",
                    "type": get_name("Regions"),
                    "title": region_title(canvas, xyhw),
                    "url": gen_iiif_url(img, res=f"{xyhw}/full/0"),
                    "canvas": canvas,
                    "xyhw": xyhw.split(","),
                    "img": img,
                }
            else:
                r_annos.append((canvas, xyhw, f"{img_name}_{canvas.zfill(nb_len)}"))
        except Exception as e:
            log(f"[get_regions_annotations]: Failed to parse annotation {anno}", e)
            continue

    # if min_c is not None:
    #     min_c = min_c or 1
    #     for canvas in range(min_c, max_c):
    #         canvas = str(canvas)
    #         if canvas not in r_annos:
    #             r_annos[canvas] = {"empty": {"img": f"{img_name}_{canvas.zfill(nb_len)}"}}

    return r_annos


def reindex_file(filename):
    a_ref = filename.replace(".txt", "")
    ref = parse_ref(a_ref)
    if not ref or not ref["regions"]:
        # if there is no regions_id in the ref, pass
        return False, a_ref
    regions_id = ref["regions"][1]
    regions = Regions.objects.filter(pk=regions_id).first()
    if not regions:
        digit = Digitization.objects.filter(pk=ref["digit"][1]).first()
        if not digit:
            # if there is no digit corresponding to the ref, pass
            return False, a_ref
        # create new Regions record if none existing
        regions = Regions(id=regions_id, digitization=digit, model="CHANGE THIS VALUE")
        regions.save()

    from app.webapp.tasks import reindex_from_file

    reindex_from_file.delay(regions_id)
    return True, a_ref


def unindex_annotation(annotation_id, remove_from_annotation_ids=False):
    http_sas = SAS_APP_URL.replace("https", "http")

    # if remove_from_annotation_ids:
    #     id_annotation = re.search(r"_anno(\d+)", annotation_id).group(1)
    #     # TODO remove from annotation.annotation_ids when it is only one annotation that is deleted

    # annotation_id = f"{wit_abbr}{wit_id}_{digit_abbr}{digit_id}_anno{regions_id}_c{canvas_nb}_{uuid4().hex[:8]}
    delete_url = (
        f"{SAS_APP_URL}/annotation/destroy?uri={http_sas}/annotation/{annotation_id}"
    )
    try:
        response = requests.delete(delete_url)
        if response.status_code == 204:
            return True
        else:
            log(
                f"[unindex_annotation] Unindex annotation request failed with status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        log(f"[unindex_annotation] Unindex annotation request failed", e)
    return False


def index_annotations_on_canvas(regions: Regions, canvas_nb):
    # this url (view canvas_annotations()) is calling format_canvas_annotations(),
    # thus returning formatted annotations for each canvas
    formatted_annos = f"{APP_URL}/{APP_NAME}/iiif/{MANIFEST_V2}/{regions.get_ref()}/list/anno-{canvas_nb}.json"
    # POST request that index the annotations
    response = urlopen(
        f"{SAS_APP_URL}/annotation/populate",
        urlencode({"uri": formatted_annos}).encode("ascii"),
    )

    if response.status != 201:
        log(
            f"[index_annotations_on_canvas] Failed to index annotations. Status: {response.status_code}",
            response.text,
        )
        return


def get_annotations_per_canvas(region: Regions, last_canvas=0, specific_canvas=""):
    """
    Returns a dict with the text annotation file info:
    { "canvas1": [ coord1, coord2 ], "canvas2": [], "canvas3": [ coord1 ] }

    if specific_canvas, returns [ coord1, coord2 ]

    coord = (x, y, width, height)
    """
    lines = get_txt_regions(region)
    if lines is None:
        log(f"[get_annotations_per_canvas] No annotation file for Regions #{region.id}")
        return {}

    annotated_canvases = {}
    current_canvas = "0"
    for line in lines:
        # if the current line concerns an img (ie: line = "img_nb img_file.jpg")
        if len(line.split()) == 2:
            current_canvas = line.split()[0]
            # TODO change, because for one specific canvas, we retrieve all the canvas before
            # TODO maybe create a json file to store annotations in another form
            if int(current_canvas) > last_canvas or specific_canvas == current_canvas:
                # if the current annotation was not already annotated, add it to the list to annotate
                # or if it is the specific canvas that we need to retrieve
                annotated_canvases[current_canvas] = []
        # if the current line contains coordinates (ie "x y width height")
        else:
            if current_canvas in annotated_canvases:
                annotated_canvases[current_canvas].append(
                    tuple(int(coord) for coord in line.split())
                )

    if specific_canvas != "":
        return (
            annotated_canvases[specific_canvas]
            if specific_canvas in annotated_canvases
            else []
        )

    return annotated_canvases


def format_canvas_annotations(regions: Regions, canvas_nb):
    canvas_annotations = get_annotations_per_canvas(
        regions, specific_canvas=str(canvas_nb)
    )
    if len(canvas_annotations) == 0:
        return {"@type": "sc:AnnotationList", "resources": []}

    return {
        "@type": "sc:AnnotationList",
        "resources": [
            format_annotation(
                regions,
                canvas_nb,
                canvas_annotations[annotation_num],
            )
            for annotation_num in range(len(canvas_annotations))
        ],
    }


def format_annotation(regions: Regions, canvas_nb, xywh):
    base_url = regions.gen_manifest_url(only_base=True, version=MANIFEST_V2)
    x, y, w, h = xywh

    width = w // 2
    height = h // 2

    annotation_id = regions.gen_annotation_id(canvas_nb)
    d = f"M{x} {y} h {width} v 0 h {width} v {height} v {height} h -{width} h -{width} v -{height}Z"
    r_id = f"rectangle_{annotation_id}"
    d_paper = "{&quot;strokeWidth&quot;:1,&quot;rotation&quot;:0,&quot;annotation&quot;:null,&quot;nonHoverStrokeColor&quot;:[&quot;Color&quot;,0,1,0],&quot;editable&quot;:true,&quot;deleteIcon&quot;:null,&quot;rotationIcon&quot;:null,&quot;group&quot;:null}"

    path = f"""<path xmlns='http://www.w3.org/2000/svg'
                    d='{d}'
                    id='{r_id}'
                    data-paper-data='{d_paper}'
                    fill-opacity='0'
                    fill='#00ff00'
                    fill-rule='nonzero'
                    stroke='#00ff00'
                    stroke-width='1'
                    stroke-linecap='butt'
                    stroke-linejoin='miter'
                    stroke-miterlimit='10'
                    stroke-dashoffset='0'
                    style='mix-blend-mode: normal'/>"""
    path = re.sub(r"\s+", " ", path).strip()

    return {
        "@id": f"{SAS_APP_URL.replace('https', 'http')}/annotation/{annotation_id}",
        "@type": "oa:Annotation",
        "dcterms:created": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "dcterms:modified": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "resource": [
            {
                "@type": "dctypes:Text",
                f"{SAS_APP_URL}/full_text": "",
                "format": "text/html",
                "chars": "<p></p>",
            }
        ],
        "on": [
            {
                "@type": "oa:SpecificResource",
                "within": {
                    "@id": f"{base_url}/manifest.json",
                    "@type": "sc:Manifest",
                },
                "selector": {
                    "@type": "oa:Choice",
                    "default": {
                        "@type": "oa:FragmentSelector",
                        "value": f"xywh={x},{y},{w},{h}",
                    },
                    "item": {
                        "@type": "oa:SvgSelector",
                        "value": f'<svg xmlns="http://www.w3.org/2000/svg">{path}</svg>',
                    },
                },
                "full": f"{base_url}/canvas/c{canvas_nb}.json",
            }
        ],
        "motivation": ["oa:commenting", "oa:tagging"],
        "@context": IIIF_CONTEXT,
    }


def set_canvas(seq, canvas_nb, img_name, img, version=None):
    """
    Build the canvas and annotation for each image
    Called for each manifest (v2: corrected annotations) image when a witness is being indexed
    """
    try:
        h, w = int(img["height"]), int(img["width"])
    except TypeError:
        h, w = img.height, img.width
    except ValueError:
        h, w = 900, 600
    # Build the canvas
    canvas = seq.canvas(ident=f"c{canvas_nb}", label=f"Page {canvas_nb}")
    canvas.set_hw(h, w)

    # Build the image annotation
    annotation = canvas.annotation(ident=f"a{canvas_nb}")
    if re.match(r"https?://(.*?)/", img_name):
        # to build hybrid manifest referencing images from other IIIF repositories
        img = annotation.image(img_name, iiif=False)
        setattr(img, "format", "image/jpeg")
    else:
        img = annotation.image(ident=img_name, iiif=True)

    img.set_hw(h, w)
    # In case we do not really index "automatic" annotations but keep them as "otherContents"
    if version == MANIFEST_V1:
        # is calling f"{APP_NAME}/iiif/{version}/{anno.get_ref()}/list/anno-{canvas_nb}.json"
        # (canvas_annotations() view) that returns formatted annotations format_canvas_annotations()
        annotation_list = canvas.annotationList(ident=f"anno-{canvas_nb}")
        annotation = annotation_list.annotation(ident=f"a-list-{canvas_nb}")
        annotation.text("Annotation")


def get_indexed_manifests():
    try:
        r = requests.get(f"{SAS_APP_URL}/manifests")
        manifests = r.json()["manifests"]
    except Exception as e:
        log(f"[get_indexed_manifests]: Failed to load indexed manifests in SAS", e)
        return False
    return [m["@id"] for m in manifests]


def index_manifest_in_sas(manifest_url, reindex=False):
    if not reindex:
        manifests = get_indexed_manifests()
        if manifests and manifest_url in manifests:
            # if the manifest was already indexed
            return True

    try:
        manifest = requests.get(manifest_url)
        manifest_content = manifest.json()
    except Exception as e:
        log(f"[index_manifest_in_sas]: Failed to load manifest for {manifest_url}", e)
        return False

    try:
        # Index the manifest into SAS
        r = requests.post(f"{SAS_APP_URL}/manifests", json=manifest_content)
        print(r)
        if r.status_code != 200:
            log(
                f"[index_manifest_in_sas] Failed to index manifest. Status code: {r.status_code}: {r.text}"
            )
            return False
    except Exception as e:
        log(
            f"[index_manifest_in_sas]: Failed to index manifest {manifest_url} in SAS",
            e,
        )
        return False
    return True


def get_canvas_list(regions: Regions, all_img=False):
    imgs = regions.get_imgs()
    if all_img:
        # Display all images associated to the digitization, even if no regions were extracted
        return [(int(img.split("_")[-1].split(".")[0]), img) for img in imgs]

    lines = get_txt_regions(regions)
    if not lines:
        log(f"[get_canvas_list] No regions file for regions #{regions.id}")
        return {
            "error": "the regions file was not yet generated"
        }  # TODO find a way to display error msg

    canvases = []
    for line in lines:
        # if the current line concerns an img (ie: line = "img_nb img_file.jpg")
        if len(line.split()) == 2:
            _, img_file = line.split()
            # use the image number as canvas number because it is more reliable that the one provided in the anno file
            canvas_nb = int(img_file.split("_")[-1].split(".")[0])
            if img_file in imgs:
                canvases.append((canvas_nb, img_file))

    return canvases


def get_canvas_lists(digit: Digitization, all_img=False):
    canvases = []
    for regions in digit.get_regions():
        canvases.extend(get_canvas_list(regions, all_img))
    return canvases


def get_indexed_annotations(regions: Regions):
    # not used
    annotations = {}
    for canvas_nb, _ in get_canvas_list(regions):
        annotations[canvas_nb] = get_indexed_canvas_annotations(regions, canvas_nb)
    return annotations


def get_indexed_canvas_annotations(regions: Regions, canvas_nb):
    try:
        response = urlopen(
            f"{SAS_APP_URL}/annotation/search?uri={regions.gen_manifest_url(only_base=True, version=MANIFEST_V2)}/canvas/c{canvas_nb}.json"
        )
        return json.loads(response.read())
    except Exception as e:
        log(
            f"[get_indexed_canvas_annotations] Could not retrieve annotation for regions #{regions.id}",
            e,
        )
        return []


def get_coord_from_annotation(sas_annotation):
    try:
        # coord => "x,y,w,h"
        coord = (sas_annotation["on"][0]["selector"]["default"]["value"]).split("=")[1]
        # remove negative values if some of the coordinates exceed the image boundaries
        return ",".join(["0" if int(num) < 0 else num for num in coord.split(",")])
    except Exception as e:
        log(
            f"[get_coord_from_annotation] Could not retrieve coord from SAS annotation",
            e,
        )
        return "0,0,0,0"


def get_id_from_annotation(sas_annotation):
    try:
        # annotation_id => "{wit_abbr}{wit_id}_{digit_abbr}{digit_id}_anno{regions_id}_c{canvas_nb}_{uuid4().hex[:8]}"
        return sas_annotation["@id"].split("/")[-1]
    except Exception as e:
        log(f"[get_id_from_annotation] Could not retrieve id from SAS annotation", e)
        return ""


def formatted_annotations(regions: Regions):
    canvas_annotations = []
    annotation_ids = []

    # TODO: here allow to display images that are not present in the regions file

    try:
        for canvas_nb, img_file in get_canvas_list(regions):
            c_annotations = get_indexed_canvas_annotations(regions, canvas_nb)
            coord_annotations = []

            if bool(c_annotations):
                coord_annotations = [
                    (
                        get_coord_from_annotation(sas_anno),
                        get_id_from_annotation(sas_anno),
                    )
                    for sas_anno in c_annotations
                ]
                annotation_ids.extend(
                    annotation_id for _, annotation_id in coord_annotations
                )

            canvas_annotations.append((canvas_nb, coord_annotations, img_file))
    except ValueError as e:
        log(
            f"[formatted_annotations] Error when generating automatic annotation list (probably no annotation file)",
            e,
        )

    return annotation_ids, canvas_annotations


def get_manifest_annotations(regions: Regions):
    try:
        response = requests.get(f"{SAS_APP_URL}/search-api/{regions.get_ref()}/search")
        annotations = response.json()

        if response.status_code != 200:
            log(
                f"[get_manifest_annotations] Failed to get annotations from SAS: {response.status_code}"
            )
            return []
    except requests.exceptions.RequestException as e:
        log(f"[get_manifest_annotations] Failed to retrieve annotations", e)
        return []

    if "resources" not in annotations or len(annotations["resources"]) == 0:
        return []

    try:
        manifest_annotations = [
            annotation["@id"] for annotation in annotations["resources"]
        ]
    except Exception as e:
        log(f"[get_manifest_annotations] Failed to parse annotations", e)
        return []

    return manifest_annotations


def check_indexation(regions: Regions, reindex=False):
    lines = get_txt_regions(regions)

    if not lines:
        return False

    if not index_manifest_in_sas(regions.gen_manifest_url(version=MANIFEST_V2)):
        return False

    generated_annotations = 0
    indexed_annotations = 0

    sas_annotations_ids = []
    try:
        for line in lines:
            line_el = line.split()
            if len(line_el) == 2:
                # if line = "canvas_nb img_name"
                canvas_nb = line_el[0]
                sas_annotations = get_indexed_canvas_annotations(regions, canvas_nb)
                nb_annotations = len(sas_annotations)

                if nb_annotations != 0:
                    indexed_annotations += nb_annotations
                    sas_annotations_ids.extend(
                        [
                            get_id_from_annotation(sas_annotation)
                            for sas_annotation in sas_annotations
                        ]
                    )
                else:
                    if not index_manifest_in_sas(
                        regions.gen_manifest_url(version=MANIFEST_V2)
                    ):
                        return False
            elif len(line_el) == 4:
                # if line = "x y w h"
                generated_annotations += 1
    except Exception as e:
        log(
            f"[check_indexation] Failed to check indexation for regions #{regions.id}",
            e,
        )
        return False

    if generated_annotations != indexed_annotations:
        for sas_annotation_id in sas_annotations_ids:
            unindex_annotation(sas_annotation_id)
        if reindex:
            if index_regions(regions):
                log(f"[check_indexation] Regions #{regions.id} were reindexed")
                return True
    return True


def get_images_annotations(regions: Regions):
    # Used to export images annotations
    imgs = []

    try:
        for canvas_nb, img_file in get_canvas_list(regions):
            c_annotations = get_indexed_canvas_annotations(regions, canvas_nb)

            if bool(c_annotations):
                canvas_imgs = [
                    f"{CANTALOUPE_APP_URL}/iiif/2/{img_file}/{get_coord_from_annotation(sas_annotation)}/full/0/default.jpg"
                    for sas_annotation in c_annotations
                ]
                imgs.extend(canvas_imgs)
    except ValueError as e:
        log(f"[get_images_annotations] Error when retrieving SAS annotations", e)

    return imgs


def delete_regions(regions: Regions):
    index_manifest_in_sas(regions.gen_manifest_url(version=MANIFEST_V2))
    sas_annotation_id = 0
    try:
        for sas_annotation in get_manifest_annotations(regions):
            sas_annotation_id = sas_annotation.split("/")[-1]
            unindex_annotation(sas_annotation_id)
    except Exception as e:
        log(
            f"[delete_regions] Failed to unindex SAS annotation #{sas_annotation_id}", e
        )
        return False

    try:
        # Delete the regions record in the database
        regions.delete()
    except Exception as e:
        log(f"[delete_regions] Failed to delete regions record #{regions.id}", e)
        return False

    return True


def get_training_regions(regions: Regions):
    # Returns a list of tuples [(file_name, file_content), (...)]
    filenames_contents = []
    for canvas_nb, img_file in get_canvas_list(regions):
        sas_annotations = get_indexed_canvas_annotations(regions, canvas_nb)
        img = Image.open(f"{IMG_PATH}/{img_file}")
        width, height = img.size
        if bool(sas_annotations):
            train_regions = []
            for sas_annotation in sas_annotations:
                x, y, w, h = [
                    int(n) for n in get_coord_from_annotation(sas_annotation).split(",")
                ]
                train_regions.append(
                    f"0 {((x + x + w) / 2) / width} {((y + y + h) / 2) / height} {w / width} {h / height}"
                )

            filenames_contents.append(
                (f"{img_file}".replace(".jpg", ".txt"), "\n".join(train_regions))
            )
    return filenames_contents


def process_regions(regions_file_content, digit, treatment_id, model="Unknown model"):
    treatment = Treatment.objects.filter(pk=treatment_id).first()

    try:
        # TODO add step to check if regions weren't generated before for the same model
        regions = Regions(digitization=digit, model=model)
        regions.save()
    except Exception as e:
        log(f"[process_regions] Create regions record for digit #{digit.id}", e)
        return False

    try:
        with open(f"{REGIONS_PATH}/{regions.get_ref()}.txt", "w+b") as f:
            f.write(regions_file_content.encode("utf-8"))
    except Exception as e:
        treatment.error_treatment(e)
        log(
            f"[process_regions] Failed to save received regions file for digit #{digit.id}",
            e,
        )
        return False

    try:
        index_regions(regions)
    except Exception as e:
        treatment.error_treatment(e)
        log(f"[process_regions] Failed to index regions for digit #{digit.id}", e)
        return False

    treatment.complete_treatment(regions.get_ref())
    return True
