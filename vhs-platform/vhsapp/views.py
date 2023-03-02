import json
import csv
import PyPDF2
import environ
from urllib.request import urlopen
from urllib.parse import urlencode
from PIL import Image
from pikepdf import Pdf
from glob import glob
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from vhs.settings import VHS_APP_URL, CANTALOUPE_APP_URL, SAS_APP_URL
from vhsapp.models import Manuscript, Volume
from vhsapp.utils.constants import (
    APP_NAME,
    APP_NAME_UPPER,
    MANUSCRIPT,
    MANUSCRIPT_ABBR,
    VOLUME,
    VOLUME_ABBR,
    APP_DESCRIPTION,
)
from vhsapp.utils.functions import credentials
from iiif_prezi.factory import ManifestFactory

from vhsapp.utils.iiif import annotate_canvas
from vhsapp.utils.paths import (
    MEDIA_PATH,
    VOL_ANNO_PATH,
    MS_ANNO_PATH,
    IMG_PATH,
)

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR / "vhs" / ".env"))


def admin_vhs(request):
    return redirect("admin:index")


"""
Build a manuscript manifest using iiif-prezi library 
IIIF Presentation API 2.0
"""


def manifest_manuscript(request, id, version):
    try:
        manuscript = Manuscript.objects.get(pk=id)
    except Manuscript.DoesNotExist:
        raise Http404("Le manuscrit #%s n'existe pas" % id)

    # Configure the factory
    fac = ManifestFactory()
    fac.set_base_prezi_uri(
        VHS_APP_URL
        + "vhs/iiif/"
        + version
        + "/"
        + MANUSCRIPT
        + "/"
        + MANUSCRIPT_ABBR
        + "-"
        + str(id)
        + "/"
    )
    fac.set_base_image_uri(CANTALOUPE_APP_URL + "iiif/2/")
    fac.set_iiif_image_info(version="2.0", lvl="2")

    # Build the manifest
    mf = fac.manifest(ident="manifest", label=manuscript.work.title)
    mf.set_metadata({"Author": manuscript.author.name})
    mf.set_metadata({"Place of conservation": manuscript.conservation_place})
    mf.set_metadata({"Reference number": manuscript.reference_number})
    mf.set_metadata({"Date (century)": manuscript.date_century})
    if date_free := manuscript.date_free:
        mf.set_metadata({"Date": date_free})
    mf.set_metadata({"Sheet(s)": manuscript.sheets})
    if origin_place := manuscript.origin_place:
        mf.set_metadata({"Place of origin": origin_place})
    if remarks := manuscript.remarks:
        mf.set_metadata({"Remarks": remarks})
    if copyists := manuscript.copyists:
        mf.set_metadata({"Copyist(s)": copyists})
    if miniaturists := manuscript.miniaturists:
        mf.set_metadata({"Miniaturist(s)": miniaturists})
    if digitized_version := manuscript.digitized_version:
        mf.set_metadata({"Source of the digitized version": digitized_version.source})
    if pinakes_link := manuscript.pinakes_link:
        mf.set_metadata(
            {"Link to Pinakes (greek mss) or Medium-IRHT (latin mss)": pinakes_link}
        )
    mf.attribution = f"{APP_NAME_UPPER} platform"
    mf.description = APP_DESCRIPTION
    mf.viewingHint = "individuals"

    # And walk through the pages
    seq = mf.sequence(ident="normal", label="Normal Order")
    if images := manuscript.imagemanuscript_set.all():
        for i, img in enumerate(images):
            i += 1
            image = Image.open(img.image)
            # Build the canvas
            cvs = seq.canvas(ident="c%s" % i, label="Folio %s" % i)
            cvs.set_hw(image.height, image.width)
            # Build the image annotation
            anno = cvs.annotation(ident="a%s" % i)
            img = anno.image(ident=img.image.url.split("/")[-1], iiif=True)
            img.set_hw(image.height, image.width)
            if version == "auto":
                annoList = cvs.annotationList(ident="anno-%s" % i)
                anno = annoList.annotation(ident="a-list-%s" % i)
                anno.text("Annotation")
    elif pdf_first := manuscript.pdfmanuscript_set.first():
        pdf_file = open(f"{MEDIA_PATH}{pdf_first.pdf}", "rb")
        readpdf = PyPDF2.PdfFileReader(pdf_file)
        total_pages = readpdf.numPages
        for image_counter in range(1, total_pages + 1):
            image_path = (
                str(pdf_first.pdf)
                .split("/")[-1]
                .replace(".pdf", "_{:04d}".format(image_counter) + ".jpg")
            )
            image = Image.open(f"{MEDIA_PATH}{IMG_PATH}{image_path}")
            # Build the canvas
            cvs = seq.canvas(
                ident="c%s" % image_counter, label="Folio %s" % image_counter
            )
            cvs.set_hw(image.height, image.width)
            # Build the image annotation
            anno = cvs.annotation(ident="a%s" % image_counter)
            img = anno.image(ident=image_path, iiif=True)
            img.set_hw(image.height, image.width)
            if version == "auto":
                annoList = cvs.annotationList(ident="anno-%s" % image_counter)
                anno = annoList.annotation(ident="a-list-%s" % image_counter)
                anno.text("Annotation")
    elif manifest_first := manuscript.manifestmanuscript_set.first():
        for image_counter, path in enumerate(
            sorted(glob(f"{MEDIA_PATH}{IMG_PATH}ms{id}_*.jpg"))
        ):
            image_counter += 1
            image_path = path.replace("\\", "/").split("/")[-1]
            image = Image.open(path)
            # Build the canvas
            cvs = seq.canvas(
                ident="c%s" % image_counter, label="Folio %s" % image_counter
            )
            cvs.set_hw(image.height, image.width)
            # Build the image annotation
            anno = cvs.annotation(ident="a%s" % image_counter)
            img = anno.image(ident=image_path, iiif=True)
            img.set_hw(image.height, image.width)
            if version == "auto":
                annoList = cvs.annotationList(ident="anno-%s" % image_counter)
                anno = annoList.annotation(ident="a-list-%s" % image_counter)
                anno.text("Annotation")
    else:
        raise Exception("There is no manifest!")

    data = mf.toJSON(top=True)

    return JsonResponse(data)


"""
Build a volume manifest using iiif-prezi library 
IIIF Presentation API 2.0
"""


def manifest_volume(request, id, version):
    try:
        volume = Volume.objects.get(pk=id)
    except Volume.DoesNotExist:
        raise Http404("Le volume #%s n'existe pas" % id)

    # Configure the factory
    fac = ManifestFactory()
    fac.set_base_prezi_uri(
        VHS_APP_URL
        + "vhs/iiif/"
        + version
        + "/"
        + VOLUME
        + "/"
        + VOLUME_ABBR
        + "-"
        + str(id)
        + "/"
    )
    fac.set_base_image_uri(CANTALOUPE_APP_URL + "iiif/2/")
    fac.set_iiif_image_info(version="2.0", lvl="2")

    # Build the manifest
    mf = fac.manifest(ident="manifest", label=volume.title)
    if author := volume.printed.author:
        mf.set_metadata({"Author": author.name})
    mf.set_metadata({"Description of work": volume.printed.description})
    if descriptive_elements := volume.printed.descriptive_elements:
        mf.set_metadata({"Descriptive elements of the content": descriptive_elements})
    if illustrators := volume.printed.illustrators:
        mf.set_metadata({"Illustrator(s)": illustrators})
    if engravers := volume.printed.engravers:
        mf.set_metadata({"Engraver(s)": engravers})
    mf.set_metadata({"Number or identifier of volume": volume.number_identifier})
    mf.set_metadata({"Place": volume.place})
    mf.set_metadata({"Date": volume.date})
    mf.set_metadata({"Publishers/booksellers": volume.publishers_booksellers})
    if digitized_version := volume.digitized_version:
        mf.set_metadata({"Source of the digitized version": digitized_version.source})
    if comment := volume.comment:
        mf.set_metadata({"Comment": comment})
    if other_copies := volume.other_copies:
        mf.set_metadata({"Other copy(ies)": other_copies})
    mf.attribution = f"{APP_NAME_UPPER} platform"
    mf.description = APP_DESCRIPTION
    mf.viewingHint = "individuals"

    # And walk through the pages
    seq = mf.sequence(ident="normal", label="Normal Order")
    if images := volume.imagevolume_set.all():
        for i, img in enumerate(images):
            i += 1
            image = Image.open(img.image)
            # Build the canvas
            cvs = seq.canvas(ident="c%s" % i, label="Page %s" % i)
            cvs.set_hw(image.height, image.width)
            # Build the image annotation
            anno = cvs.annotation(ident="a%s" % i)
            img = anno.image(ident=img.image.url.split("/")[-1], iiif=True)
            img.set_hw(image.height, image.width)
            if version == "auto":
                annoList = cvs.annotationList(ident="anno-%s" % i)
                anno = annoList.annotation(ident="a-list-%s" % i)
                anno.text("Annotation")
    elif pdf_first := volume.pdfvolume_set.first():
        pdf_file = Pdf.open(f"{MEDIA_PATH}{pdf_first.pdf}")
        total_pages = len(pdf_file.pages)
        for image_counter in range(1, total_pages + 1):
            image_path = (
                str(pdf_first)
                .split("/")[-1]
                .replace(".pdf", "_{:04d}".format(image_counter) + ".jpg")
            )
            image = Image.open(f"{MEDIA_PATH}{IMG_PATH}{image_path}")
            # Build the canvas
            cvs = seq.canvas(
                ident="c%s" % image_counter, label="Page %s" % image_counter
            )
            cvs.set_hw(image.height, image.width)
            # Build the image annotation
            anno = cvs.annotation(ident="a%s" % image_counter)
            img = anno.image(ident=image_path, iiif=True)
            img.set_hw(image.height, image.width)
            if version == "auto":
                annoList = cvs.annotationList(ident="anno-%s" % image_counter)
                anno = annoList.annotation(ident="a-list-%s" % image_counter)
                anno.text("Annotation")
    elif manifest_first := volume.manifestvolume_set.first():
        for image_counter, path in enumerate(
            sorted(glob(f"{MEDIA_PATH}{IMG_PATH}vol{id}_*.jpg"))
        ):
            image_counter += 1
            image_path = path.replace("\\", "/").split("/")[-1]
            image = Image.open(path)
            # Build the canvas
            cvs = seq.canvas(
                ident="c%s" % image_counter, label="Page %s" % image_counter
            )
            cvs.set_hw(image.height, image.width)
            # Build the image annotation
            anno = cvs.annotation(ident="a%s" % image_counter)
            img = anno.image(ident=image_path, iiif=True)
            img.set_hw(image.height, image.width)
            if version == "auto":
                annoList = cvs.annotationList(ident="anno-%s" % image_counter)
                anno = annoList.annotation(ident="a-list-%s" % image_counter)
                anno.text("Annotation")
    else:
        raise Exception("There is no manifest!")

    data = mf.toJSON(top=True)

    return JsonResponse(data)


def annotation_auto(request, id, work):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        "attachment; filename=annotations_iiif_" + work + "_" + str(id) + ".csv"
    )
    writer = csv.writer(response)
    writer.writerow(["IIIF_Image_Annotations"])
    annotations_path = (
        VOL_ANNO_PATH if work == VOLUME else MS_ANNO_PATH
    )
    with open(f"{MEDIA_PATH}{annotations_path}{id}.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            if len(line.split()) == 2:
                img_name = line.split()[1]
            else:
                region = (
                    line.split()[0]
                    + ","
                    + line.split()[1]
                    + ","
                    + line.split()[2]
                    + ","
                    + line.split()[3]
                )
                writer.writerow(
                    [
                        CANTALOUPE_APP_URL
                        + "iiif/2/"
                        + img_name
                        + "/"
                        + region
                        + "/full/0/default.jpg"
                    ]
                )
    return response


def annotate_work(request, id, version, work, work_abbr, canvas):
    annotations_path = (
        VOL_ANNO_PATH if work == VOLUME else MS_ANNO_PATH
    )
    with open(f"{MEDIA_PATH}{annotations_path}{id}.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        nbr_anno = 0
        list_anno = []
        check = False
        for line in lines:
            if len(line.split()) == 2 and line.split()[0] == str(canvas):
                check = True
                continue
            if check:
                if len(line.split()) == 4:
                    nbr_anno += 1
                    list_anno.append(tuple(int(item) for item in tuple(line.split())))
                else:
                    break
    data = {
        "@type": "sc:AnnotationList",
        "resources": [
            annotate_canvas(
                id, version, work, work_abbr, canvas, list_anno[num_anno], num_anno
            )
            for num_anno in range(nbr_anno)
            if nbr_anno > 0
        ],
    }
    return JsonResponse(data)


"""
Populate annotation store from IIIF Annotation List
"""


def populate_annotation(request, id, work):
    work_map = {
        VOLUME: (VOLUME_ABBR, VOL_ANNO_PATH),
        MANUSCRIPT: (MANUSCRIPT_ABBR, MS_ANNO_PATH),
    }
    work_abbr, annotations_path = work_map.get(work, (None, None))
    if not env("DEBUG"):
        credentials(SAS_APP_URL, env("SAS_USERNAME"), env("SAS_PASSWORD"))
    with open(f"{MEDIA_PATH}{annotations_path}{id}.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    canvas = [line.split()[0] for line in lines if len(line.split()) == 2]
    for c in canvas:
        url_search = (
            SAS_APP_URL
            + "annotation/search?uri="
            + VHS_APP_URL
            + "vhs/iiif/v2/"
            + work
            + "/"
            + work_abbr
            + "-"
            + str(id)
            + "/canvas/c"
            + c
            + ".json"
        )
        # Store the response of URL
        response = urlopen(url_search)
        # Store the JSON response from url in data
        data = json.loads(response.read())
        if len(data) > 0:
            return HttpResponse(status=200)
    url_populate = SAS_APP_URL + "annotation/populate"
    for line in lines:
        if len(line.split()) == 2:
            canvas = line.split()[0]
            params = {
                "uri": VHS_APP_URL
                + "vhs/iiif/v2/"
                + work
                + "/"
                + work_abbr
                + "-"
                + str(id)
                + "/list/anno-"
                + canvas
                + ".json",
            }
            query_string = urlencode(params)
            data = query_string.encode("ascii")
            response = urlopen(url_populate, data)  # This will make the method "POST"

    return HttpResponse(status=200)


@login_required(login_url=f"/{APP_NAME}-admin/")
def show_work(request, id, work):
    work_map = {
        MANUSCRIPT: (Manuscript, MANUSCRIPT_ABBR, MS_ANNO_PATH),
        VOLUME: (Volume, VOLUME_ABBR, VOL_ANNO_PATH),
    }
    work_model, work_abbr, annotations_path = work_map.get(work, (None, None, None))
    work_obj = get_object_or_404(work_model, pk=id)
    url_manifest = (
        VHS_APP_URL
        + "vhs/iiif/v2/"
        + work
        + "/"
        + work_abbr
        + "-"
        + str(id)
        + "/manifest.json"
    )
    canvas_annos = []
    if not env("DEBUG"):
        credentials(SAS_APP_URL, env("SAS_USERNAME"), env("SAS_PASSWORD"))
    with open(f"{MEDIA_PATH}{annotations_path}{id}.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            if len(line.split()) == 2:
                url_search = (
                    SAS_APP_URL
                    + "annotation/search?uri="
                    + VHS_APP_URL
                    + "vhs/iiif/v2/"
                    + work
                    + "/"
                    + work_abbr
                    + "-"
                    + str(id)
                    + "/canvas/c"
                    + str(line.split()[0])
                    + ".json"
                )
                # Store the response of URL
                response = urlopen(url_search)
                # Store the JSON response from url in data
                data = json.loads(response.read())
                annos = [
                    (
                        (d["on"][0]["selector"]["default"]["value"]).split("=")[1],
                        d["@id"].split("/")[-1],
                    )
                    for d in data
                    if len(data) > 0
                ]
                canvas_annos.append(
                    (
                        annos,
                        CANTALOUPE_APP_URL
                        + "iiif/2/"
                        + line.split()[1]
                        + "/full/full/0/default.jpg",
                    )
                )
    return render(
        request,
        "vhsapp/show.html",
        context={
            "work": work,
            "work_obj": work_obj,
            "canvas_annos": canvas_annos,
            "url_manifest": url_manifest,
        },
    )
