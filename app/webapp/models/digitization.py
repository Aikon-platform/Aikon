import os
from glob import glob

from django.db import models
from django.utils.safestring import mark_safe

from app.webapp.models.utils.functions import get_fieldname

import threading
from uuid import uuid4
from io import BytesIO
from django.core.files import File

from PIL import Image
from functools import partial

from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from pdf2image import convert_from_path

from app.webapp.utils.iiif.gen_html import gen_manifest_btn
from app.webapp.utils.logger import log, console

from app.webapp.models.utils.constants import (
    MANIFEST,
    MS_ABBR,
    VOL_ABBR,
    IMG_INFO,
    MANIFEST_INFO,
    MS,
    VOL,
    WIT,
    DIGIT_TYPE,
    IMG,
    PDF,
    MANIFEST,
)
from app.webapp.utils.functions import (
    get_last_file,
    get_icon,
    pdf_to_img,
    to_jpg,
    anno_btn,
)
from app.webapp.utils.paths import (
    BASE_DIR,
    IMG_PATH,
    MEDIA_DIR,
    IMG_DIR,
    ANNO_PATH,
)

from app.webapp.utils.iiif.validation import validate_manifest
from app.webapp.utils.iiif.download import extract_images_from_iiif_manifest

from app.webapp.models.witness import Witness


def get_name(fieldname, plural=False):
    fields = {
        "source": {"en": "digitization source", "fr": "source de la numérisation"},
        "manifest_v1": {
            "en": "automatic annotations",
            "fr": "annotations automatiques",
        },
        "manifest_v2": {"en": "corrected annotations", "fr": "annotations corrigées"},
        "is_validated": {"en": "validate annotations", "fr": "valider les annotations"},
        "is_validated_info": {
            "en": "annotations will no longer be editable",
            "fr": "les annotations ne seront plus modifiables",
        },
    }
    return get_fieldname(fieldname, fields, plural)


def rename_file(digitization, original_filename):
    """
    Rename the file using its witness id and specific id
    The file will be uploaded to "{path}/{filename}.{ext}"
    """
    digitization.ext = original_filename.split(".")[-1]
    new_filename = digitization.get_filename()
    # TODO: create fct that do not erase the file if a image was already recorded with the same name
    return f"{digitization.get_relative_path()}/{new_filename}.{digitization.ext}"


class Digitization(models.Model):
    class Meta:
        verbose_name = get_name("Digitization")
        verbose_name_plural = get_name("Digitization", True)
        app_label = "webapp"

    def __init__(self, nb=None, ext=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nb = nb
        self.ext = ext

    def __str__(self):
        return f"{self.get_digit_type().capitalize()} #{self.id} | {self.witness.__str__()}"

    witness = models.ForeignKey(Witness, on_delete=models.CASCADE)
    digit_type = models.CharField(
        verbose_name=get_name("type"), choices=DIGIT_TYPE, max_length=150
    )

    image = models.ImageField(
        verbose_name=IMG,
        upload_to=partial(rename_file),
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "tif"])
        ],
        help_text=IMG_INFO,
    )
    pdf = models.FileField(
        verbose_name=PDF,
        upload_to=partial(rename_file),
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    manifest = models.URLField(
        verbose_name=MANIFEST,
        help_text=MANIFEST_INFO,
        validators=[validate_manifest],
    )
    is_validated = models.BooleanField(
        verbose_name=get_name("is_validated"),
        default=False,
        help_text=f"{get_icon('triangle-exclamation', '#efb80b')} {get_name('is_validated_info')}",
    )

    def get_witness(self) -> Witness | None:
        try:
            return self.witness
        except AttributeError:
            return None

    def get_wit_type(self):
        witness = self.get_witness()
        return witness.type

    def get_wit_prefix(self):
        witness = self.get_witness()
        if witness:
            return f"{witness.get_ref()}"
        return ""

    def get_digit_type(self):
        # NOTE should be returning "image" / "pdf" / "manifest"
        return str(self.digit_type)

    def get_annotations(self):
        return self.annotation_set.all()

    def get_filename(self):
        """
        Returns filename without extension
        """
        # OLD return self.pdf.name.split("/")[-1].split(".")[0]
        # e.g. self.pdf.name = "pdf/filename.pdf" => filename = "filename"
        try:
            return f"{self.get_wit_prefix()}_{self.id}"
        except Exception:
            return None

    def get_anno_filenames(self):
        anno_files = []
        for anno in self.get_annotations():
            anno_files.append(anno.get_filename())
        return anno_files

    def has_annotations(self):
        # if there is at least one annotation record and its associated annotation file
        for anno_file in self.get_anno_filenames():
            if len(glob(f"{BASE_DIR}/{ANNO_PATH}/{anno_file}.txt")) > 0:
                return True
        return False

    def get_imgs(self):
        imgs = []
        for filename in os.listdir(IMG_PATH):
            if filename.startswith(self.get_filename()):
                imgs.append(filename)
        return imgs

    def has_manifest(self):
        # check if at least one file begins with the correct filename prefix
        for entry in os.scandir(IMG_PATH):
            if entry.name.startswith(self.get_filename()) and entry.is_file():
                return True
        return False

    def save(self, *args, **kwargs):
        digit_type = self.get_digit_type()

        if digit_type == IMG:
            ext = self.image.name.split(".")[1]
            if ext != "jpg" and ext != "jpeg":
                # TODO check how it does for multiple images
                to_jpg(self.image)
            super().save(*args, **kwargs)

        elif digit_type == PDF:
            super().save(*args, **kwargs)
            # Run the PDF to image async conversion task in the background using threading
            t = threading.Thread(target=pdf_to_img)
            t.start()

        elif digit_type == MANIFEST:
            super().save(*args, **kwargs)
            # Run the async extraction of images from IIIF using threading
            t = threading.Thread(
                target=extract_images_from_iiif_manifest,
                args=(self.manifest, self.get_filename()),
            )
            t.start()

    def delete(self, using=None, keep_parents=False):
        if self.get_digit_type() == PDF:  # NOTE: maybe not for manifests
            self.pdf.storage.delete(self.get_file_path(False))
            for filename in self.get_imgs():
                try:
                    os.remove(os.path.join(IMG_PATH, filename))
                except OSError as e:
                    log(
                        f"[Digitization.delete()] Error deleting PDF images ({filename})",
                        e,
                    )
        super().delete()

    def set_ext(self, extension):
        self.ext = extension

    def get_relative_path(self):
        # must be relative to MEDIA_DIR
        return IMG_DIR

    def get_absolute_path(self):
        return f"{BASE_DIR}/{MEDIA_DIR}/{self.get_relative_path()}"

    def get_file_path(self, is_abs=True):
        path = self.get_absolute_path() if is_abs else self.get_relative_path()
        return f"{path}/{self.get_filename()}.{self.ext}"

    def get_nb_of_pages(self):
        import PyPDF2

        with open(self.get_file_path(), "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            page_nb = pdf_reader.getNumPages()
        return page_nb

        # NOTE methods to be used inside list columns of witnesses

    def anno_btn(self):
        # To display a button in the list of witnesses to know if they were annotated or not
        action = "final" if self.is_validated else "edit"
        return mark_safe(
            anno_btn(
                self.id,  # TODO handle multiple annotations files
                action if self.has_annotations() else "no_anno",
            )
        )

    def manifest_link(self):
        return gen_manifest_btn(self.id, self.get_wit_type(), self.has_manifest())

    def get_metadata(self):
        metadata = self.get_witness().get_metadata()

        # TODO finish this

        if manifest := self.manifest:
            metadata["Source manifest"] = str(manifest)
            metadata["Is annotated"] = self.has_annotations()

        return metadata


# Receive the pre_delete signal and delete the file associated with the model instance
@receiver(pre_delete, sender=Digitization)
def image_delete(sender, digit: Digitization, **kwargs):
    if digit.get_digit_type() != IMG:
        return
    # Pass False so ImageField doesn't save the model
    digit.image.delete(False)
