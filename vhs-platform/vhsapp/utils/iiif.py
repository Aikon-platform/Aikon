import os
import re

import requests
import time
from glob import glob
from datetime import datetime
from PIL import Image
from pikepdf import Pdf
from tripoli import IIIFValidator
from pathlib import Path
import shutil
from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from vhsapp.utils.constants import APP_NAME, MANIFEST_AUTO, MANIFEST_V2
from vhsapp.utils.functions import log, get_json, create_dir, console
from vhsapp.utils.paths import MEDIA_PATH, IMG_PATH, BASE_DIR
from vhsapp.utils.functions import get_icon, anno_btn
from vhsapp.models.constants import VOL_ABBR, MS_ABBR, VOL, MS
from vhs.settings import SAS_APP_URL, VHS_APP_URL, CANTALOUPE_APP_URL


IIIF_ICON = "<img alt='IIIF' src='https://iiif.io/assets/images/logos/logo-sm.png' height='15'/>"


def parse_manifest(manifest):
    url = urlparse(manifest)
    return url.hostname, url.path.strip("/").split("/")


def validate_gallica_manifest(manifest, check_hostname=True):
    """
    Validate the pattern of a Gallica manifest URL
    """
    if (
        check_hostname
        and re.match(r"https?://(.*?)/", manifest).group(1) != "gallica.bnf.fr"
    ):
        # Check if the hostname of the URL matches the desired pattern
        raise ValidationError("Not a Gallica manifest")

    # Define the regular expression pattern for a valid Gallica manifest URL
    pattern = re.compile(
        r"https://gallica.bnf.fr/iiif/ark:/12148/[a-z0-9]+/manifest.json"
    )
    # Check if the URL matches the pattern
    if not bool(pattern.match(manifest)):
        raise ValidationError("Gallica manifest URL is not valid.")


def validate_gallica_manifest_url(value):
    """
    Validate the pattern of a Gallica manifest URL
    """
    hostname = re.match(r"https?://(.*?)/", value).group(1)
    # Check if the hostname of the URL matches the desired pattern
    if hostname == "gallica.bnf.fr":
        # Define the regular expression pattern for a valid Gallica manifest URL
        pattern = re.compile(
            r"https://gallica.bnf.fr/iiif/ark:/12148/[a-z0-9]+/manifest.json"
        )
        match = bool(pattern.match(value))
        # Check if the URL matches the pattern
        if not match:
            raise ValidationError("Invalid Gallica manifest")


def validate_iiif_manifest(url):
    """
    Validate a IIIF manifest using Tripoli
    Check if the manifest conforms to the IIIF Presentation API 2.1 specification
    """
    try:
        manifest = get_json(url)
        validator = IIIFValidator()
        validator.validate(manifest)

    except Exception:
        raise ValidationError("The URL is not a valid IIIF manifest")


def validate_manifest(manifest):
    validate_iiif_manifest(manifest)
    hostname, path = parse_manifest(manifest)
    if hostname == "gallica.bnf.fr":
        validate_gallica_manifest(manifest, False)
        raise ValidationError("The URL is not a valid Gallica manifest")


def extract_images_from_iiif_manifest(manifest_url, work, width=None, height=None):
    """
    Extract all images from an IIIF manifest
    """
    manifest = get_json(manifest_url)
    size = get_formatted_size(width, height)
    if manifest is not None:
        manifest_id = Path(urlparse(get_id(manifest)).path).parent.name
        console(f"Processing {manifest_id}...")
        output_path = create_dir(BASE_DIR / IMG_PATH)
        i = 1
        for img_url in get_iiif_resources(manifest, True):
            img_id = f"{i:04d}"
            img_url = f"{img_url}/full/{size}/0/default.jpg"
            i += 1

            with requests.get(img_url, stream=True) as response:
                response.raw.decode_content = True
                output_file = output_path / f"{work}_{img_id}.jpg"
                console(f"Saving {output_file.relative_to(BASE_DIR / IMG_PATH)}...")
                time.sleep(0.1)
                try:
                    with open(output_file, mode="wb") as f:
                        shutil.copyfileobj(response.raw, f)
                        # f.write(image_response.content)
                except Exception as e:
                    log(f"Failed to extract images from {manifest_url}:\n{e}")

    # img_path = f"{BASE_DIR}/{img_path}"
    # try:
    #     manifest = get_json(manifest_url)
    #     image_counter = 1
    #     for sequence in manifest["sequences"]:
    #         for canvas in sequence["canvases"]:
    #             for image in canvas["images"]:
    #                 image_url = (
    #                     f"{image['resource']['service']['@id']}/full/full/0/default.jpg"
    #                 )
    #                 image_response = requests.get(image_url)
    #                 with open(f"{img_path}{work}_{image_counter:04d}.jpg", "wb") as f:
    #                     f.write(image_response.content)
    #                 image_counter += 1
    #                 time.sleep(0.5)


def gen_iiif_url(
    img,
    scheme="http",
    host="localhost",
    port=8182,
    vers=2,
    res="full/full/0",
    color="default",
    ext="jpg",
):
    # E.g. "http://localhost/iiif/2/image_name.jpg/full/full/0/default.jpg"
    # return f"{scheme}://{host}{f':{port}' if port else ''}/iiif/{vers}/{img}/{res}/{color}.{ext}"
    return f"{CANTALOUPE_APP_URL}/iiif/{vers}/{img}/{res}/{color}.{ext}"


def get_link_manifest(obj_id, manifest_url, tag_id="url_manifest_"):
    return f"<a id='{tag_id}{obj_id}' href='{manifest_url}' target='_blank'>{manifest_url} {IIIF_ICON}</a>"


def gen_btn(obj_id, action="VISUALIZE", vers=MANIFEST_AUTO, ps_type=VOL.lower()):
    obj_ref = f"{APP_NAME}/iiif/{vers}/{ps_type}/{obj_id}"
    manifest = f"{CANTALOUPE_APP_URL}/{obj_ref}/manifest.json"

    if vers == MANIFEST_AUTO:
        tag_id = f"iiif_auto_"
        message_id = f"message_auto_{obj_id}"
        download_url = f"/{obj_ref}/annotation/"
        anno_type = "CSV"
    else:
        tag_id = f"url_manifest_"
        message_id = f"message_{obj_id}"
        download_url = f"{SAS_APP_URL}/search-api/{obj_id}/search/"
        anno_type = "JSON"

    return mark_safe(
        f"{get_link_manifest(obj_id, manifest, tag_id)}<br>{anno_btn(obj_id, action)}"
        f'<a href="{download_url}" target="_blank">{get_icon("download")} Download annotation ({anno_type})</a>'
        f'<span id="{message_id}" style="color:#FF0000"></span>'
    )


def gen_manifest_url(
    m_id,
    scheme="http",
    host="localhost",
    port=8182,
    vers=MANIFEST_AUTO,
    m_type=VOL.lower(),
):
    # return f"{scheme}://{host}{f':{port}' if port else ''}/{APP_NAME}/iiif/{vers}/{m_type}/{m_id}/manifest.json"
    return f"{CANTALOUPE_APP_URL}/{APP_NAME}/iiif/{vers}/{m_type}/{m_id}/manifest.json"


def process_images(work, seq, version):
    """
    Process the images of a work and add them to a sequence
    """
    if hasattr(work, "imagemanuscript_set"):
        images = work.imagemanuscript_set.all()
        pdf_first = work.pdfmanuscript_set.first()
        manifest_first = work.manifestmanuscript_set.first()
        work_abbr = MS_ABBR
    else:
        images = work.imagevolume_set.all()
        pdf_first = work.pdfvolume_set.first()
        manifest_first = work.manifestvolume_set.first()
        work_abbr = VOL_ABBR
    # Check if there are any work images and process them
    if images:
        for counter, img in enumerate(images, start=1):
            image_name = img.image.url.split("/")[-1]
            image = Image.open(img.image)
            build_canvas_and_annotation(seq, counter, image_name, image, version)
    # Check if there is a PDF work and process it
    elif pdf_first:
        with Pdf.open(f"{MEDIA_PATH}{pdf_first.pdf}") as pdf_file:
            total_pages = len(pdf_file.pages)
            for counter in range(1, total_pages + 1):
                image_name = pdf_first.pdf.name.split("/")[-1].replace(
                    ".pdf", f"_{counter:04d}.jpg"
                )
                image = Image.open(f"{IMG_PATH}{image_name}")
                build_canvas_and_annotation(seq, counter, image_name, image, version)
    # Check if there is a manifest work and process it
    elif manifest_first:
        for counter, path in enumerate(
            sorted(glob(f"{IMG_PATH}{work_abbr}{work.id}_*.jpg")),
            start=1,
        ):
            image_name = os.path.basename(path)
            image = Image.open(path)
            build_canvas_and_annotation(seq, counter, image_name, image, version)
    # If none of the above, raise an exception
    else:
        raise Exception("There is no manifest!")


def build_canvas_and_annotation(seq, counter, image_name, image, version):
    """
    Build the canvas and annotation for each image
    """
    # Build the canvas
    cvs = seq.canvas(ident=f"c{counter}", label=f"Page {counter}")
    cvs.set_hw(image.height, image.width)
    # Build the image annotation
    anno = cvs.annotation(ident=f"a{counter}")
    img = anno.image(ident=image_name, iiif=True)
    img.set_hw(image.height, image.width)
    if version == "auto":
        anno_list = cvs.annotationList(ident=f"anno-{counter}")
        anno = anno_list.annotation(ident=f"a-list-{counter}")
        anno.text("Annotation")


def annotate_canvas(id, version, work, work_abbr, canvas, anno, num_anno):
    base_url = f"{VHS_APP_URL}/{APP_NAME}/iiif/{version}/{work}/{work_abbr}-{id}"

    anno2_2 = anno[2] // 2
    anno3_2 = anno[3] // 2

    data_paper = (
        '{"strokeWidth":1,"rotation":0,"deleteIcon":null,"rotationIcon":null,'
        '"group":null,"editable":true,"annotation":null}'
    )

    return {
        "@id": f"{SAS_APP_URL}/annotation/{work_abbr}-{id}-{canvas}-{num_anno + 1}",
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
                        "value": f"xywh={anno[0]},{anno[1]},{anno[2]},{anno[3]}",
                    },
                    "item": {
                        "@type": "oa:SvgSelector",
                        "value": "<svg xmlns='http://www.w3.org/2000/svg'><path xmlns='http://www.w3.org/2000/svg' "
                        f"d='M{anno[0]} {anno[1]} h {anno2_2} v 0 h {anno2_2} v {anno3_2} v {anno3_2} "
                        f"h -{anno2_2} h -{anno2_2} v -{anno3_2}Z' data-paper-data='{data_paper}'"
                        f"id='rectangle_{work_abbr}{id}-{canvas}-{num_anno + 1}' fill-opacity='0' "
                        f"fill='#00ff00' fill-rule='nonzero' stroke='#00ff00' stroke-width='1' "
                        f"stroke-linecap='butt' stroke-linejoin='miter' stroke-miterlimit='10' "
                        f"stroke-dashoffset='0' style='mix-blend-mode: normal'/></svg",
                    },
                },
                "full": f"{base_url}/canvas/c{canvas}.json",
            }
        ],
        "motivation": ["oa:commenting", "oa:tagging"],
        "@context": "http://iiif.io/api/presentation/2/context.json",
    }


def get_id(dic):
    if type(dic) == dict:
        try:
            return dic["@id"]
        except KeyError as e:
            try:
                return dic["id"]
            except KeyError as e:
                log(f"No id provided {e}")
    console(dic)

    if type(dic) == str:
        return dic

    return None


def get_canvas_img(canvas_img, only_img_url=False):
    img_url = get_id(canvas_img["resource"]["service"])
    if only_img_url:
        return img_url
    return get_img_id(canvas_img["resource"]), img_url


def get_item_img(item_img, only_img_url=False):
    img_url = get_id(item_img["body"]["service"][0])
    if only_img_url:
        return img_url
    return get_img_id(item_img), img_url


def get_img_id(img):
    img_id = get_id(img)
    if ".jpg" in img_id:
        try:
            return img_id.split("/")[-5]
        except IndexError:
            return None
        # return Path(urlparse(img_id).path).parts[-5]
    return img_id.split("/")[-1]


def get_formatted_size(width="", height=""):
    if not width and not height:
        # return "full"
        return "1000,"
    return f"{width or ''},{height or ''}"


def get_iiif_resources(manifest, only_img_url=False):
    try:
        img_list = [canvas["images"] for canvas in manifest["sequences"][0]["canvases"]]
        img_info = [
            get_canvas_img(img, only_img_url) for imgs in img_list for img in imgs
        ]
    except KeyError:
        try:
            img_list = [
                canvas["images"] for canvas in manifest["sequences"][0]["canvases"]
            ]
            img_info = [
                get_canvas_img(img, only_img_url) for imgs in img_list for img in imgs
            ]
        except KeyError:
            try:
                img_list = [
                    item
                    for items in manifest["items"]
                    for item in items["items"][0]["items"]
                ]
                img_info = [get_item_img(img) for img in img_list]
            except KeyError as e:
                console(f"Unable to retrieve resources from manifest {manifest}\n{e}")
                return []

    return img_info
