from django.utils.safestring import mark_safe

from app.webapp.models.annotation import Annotation
from app.webapp.models.digitization import Digitization
from app.webapp.utils.constants import MANIFEST_V1, MANIFEST_V2
from app.webapp.utils.functions import get_icon, get_action, cls
from app.webapp.models.utils.constants import VOL
from app.config.settings import (
    SAS_APP_URL,
    APP_URL,
    APP_NAME,
)
from app.webapp.utils.iiif import IIIF_ICON


def anno_btn(obj: Annotation | Digitization, action="view"):
    disabled = ""
    btn = f"{get_action(action, 'upper')} ANNOTATIONS"

    if action == "view":
        color = "#EFB80B"
        icon = get_icon("eye")
        # The link redirects to Mirador with no annotations (Digitization) or automatic annotations (Annotation)
        link = f"{SAS_APP_URL}/indexView.html?iiif-content={obj.gen_manifest_url(version=MANIFEST_V1)}"
        btn = "VIEW SOURCE"
    elif action == "edit":
        color = "#008CBA"
        icon = get_icon("pen-to-square")
        # The link redirects to the edit annotation page (show_annotations() view)
        link = f"{APP_URL}/{APP_NAME}/{obj.get_ref()}/show/"
    elif action == "final":
        color = "#4CAF50"
        icon = get_icon("check")
        # The link redirects to Mirador with corrected annotations (Annotation)
        link = f"{SAS_APP_URL}/indexView.html?iiif-content={obj.gen_manifest_url(version=MANIFEST_V2)}"
    else:
        # When the button is not supposed to redirects to anything
        link = "#"
        btn = get_action(action, "upper")
        color = "#878787"
        icon = get_icon("eye-slash")
        disabled = "disabled"

    return (
        f"<a href='{link}' class='btn btn-md active annotate-manifest' role='button' aria-pressed='true' target='_blank'"
        f"{disabled} style='background-color:{color};'>{icon} {btn}</a>"
    )


def get_link_manifest(obj: Annotation | Digitization, version=None):
    manifest_url = obj.gen_manifest_url(version=version)
    return f"<a id='{obj.get_ref()}' href='{manifest_url}' target='_blank'>{manifest_url} {IIIF_ICON}</a>"


def gen_btn(obj: Annotation | Digitization, action="view"):
    """
    Used to create button in the witness form
    """
    if action == "no_manifest" or action == "no_anno":
        return mark_safe(anno_btn(obj, action))

    is_anno = True
    if cls(obj) == Annotation:
        download_url = f"{SAS_APP_URL}/search-api/{obj.get_ref()}/search/"
        anno_type = "JSON"
        version = MANIFEST_V2
    elif cls(obj) == Digitization:
        download_url = f"{APP_URL}/{APP_NAME}/iiif/digit-annotation/{obj.id}"
        anno_type = "TXT"
        version = None
        is_anno = obj.has_annotations()
    else:
        return mark_safe("NOT SUPPOSED TO OCCUR")

    download = (
        f'<a href="{download_url}" target="_blank">{get_icon("download")} {get_action("download")} annotations ({anno_type})</a>'
        if is_anno
        else ""
    )

    return mark_safe(
        f"{get_link_manifest(obj, version)}<br>{anno_btn(obj, action)}<br>{download}"
    )


def gen_manifest_btn(digit: Digitization, has_manifest=True):
    manifest = digit.gen_manifest_url()
    mf = (
        f"<a href='{manifest}' target='_blank'>{IIIF_ICON}</a>"
        if has_manifest
        else "<span class='faded'>No manifest</span>"
    )
    return mark_safe(f"<div class='iiif-icon'>{mf}</div>")
