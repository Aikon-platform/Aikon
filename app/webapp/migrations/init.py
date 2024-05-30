# Generated by Django 4.0.4 on 2023-07-12 14:08

import app.webapp.models.digitization
import app.webapp.utils.iiif.validation
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import functools


def populate_languages(apps, schema_editor):
    languages = [
        {"code": "la", "lang": "Latin"},
        {"code": "he", "lang": "Hebrew"},
        {"code": "sa", "lang": "Sanskrit"},
        {"code": "grc", "lang": "Ancient greek"},
        {"code": "fa", "lang": "Persian"},
        {"code": "zh-CN", "lang": "Simplified chinese"},
        {"code": "zh-Hant", "lang": "Traditional chinese"},
    ]
    for language in languages:
        apps.get_model("webapp", "Language").objects.create(
            lang=language["lang"], code=language["code"]
        )

    # TODO: create ontology for the Tag class


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "lang",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Language"
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=200, unique=True, verbose_name="Code"),
                ),
            ],
            options={
                "verbose_name": "Language",
                "verbose_name_plural": "Language",
            },
        ),
        migrations.RunPython(populate_languages),
    ]
