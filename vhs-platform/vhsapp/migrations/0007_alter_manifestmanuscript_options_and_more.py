# Generated by Django 4.0.4 on 2023-02-22 15:07

from django.db import migrations, models
import django.db.models.deletion
import vhsapp.utils.iiif


class Migration(migrations.Migration):

    dependencies = [
        ("vhsapp", "0006_alter_manifestmanuscript_manifest_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="manifestmanuscript",
            options={
                "verbose_name": "IIIF manifest",
                "verbose_name_plural": "IIIF manifests",
            },
        ),
        migrations.AlterModelOptions(
            name="manifestvolume",
            options={
                "verbose_name": "IIIF manifest",
                "verbose_name_plural": "IIIF manifests",
            },
        ),
        migrations.AlterModelOptions(
            name="manuscript",
            options={
                "ordering": ["-conservation_place"],
                "verbose_name": "Manuscript",
                "verbose_name_plural": "Manuscripts",
            },
        ),
        migrations.RemoveField(
            model_name="manuscript",
            name="date_century",
        ),
        migrations.RemoveField(
            model_name="manuscript",
            name="work",
        ),
        migrations.AlterField(
            model_name="manifestmanuscript",
            name="manifest",
            field=models.URLField(
                help_text="<div class='tooltip'>\n                 <i class='fa-solid fa-circle-info' title='Manifest'></i>\n                 <span class='tooltiptext'>A IIIF manifest is the package that contains all the information related\n                 to a particular digital object, including the image itself as well as the metadata.</span>\n             </div>\n             E.g.: <a href='https://gallica.bnf.fr/iiif/ark:/12148/btv1b60004321/manifest.json' target='_blank'>\n             https://gallica.bnf.fr/iiif/ark:/12148/btv1b60004321/manifest.json</a>",
                validators=[vhsapp.utils.iiif.validate_manifest],
                verbose_name="Manifest",
            ),
        ),
        migrations.AlterField(
            model_name="manifestvolume",
            name="manifest",
            field=models.URLField(
                help_text="<div class='tooltip'>\n                 <i class='fa-solid fa-circle-info' title='Manifest'></i>\n                 <span class='tooltiptext'>A IIIF manifest is the package that contains all the information related\n                 to a particular digital object, including the image itself as well as the metadata.</span>\n             </div>\n             E.g.: <a href='https://gallica.bnf.fr/iiif/ark:/12148/btv1b60004321/manifest.json' target='_blank'>\n             https://gallica.bnf.fr/iiif/ark:/12148/btv1b60004321/manifest.json</a>",
                validators=[vhsapp.utils.iiif.validate_manifest],
                verbose_name="Manifest",
            ),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="author",
            field=models.ForeignKey(
                blank=True,
                help_text="<ul><li>Indiquez [Anonyme] si auteur non identifié.</li><li>Si nom auteur non trouvé, merci de chercher directement dans <a href='https://data.bnf.fr/' target='_blank'>Data BnF</a>.</li></ul>",
                max_length=200,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="vhsapp.author",
                verbose_name="Author",
            ),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="conservation_place",
            field=models.CharField(max_length=150, verbose_name="Conservation place"),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="copyists",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="Copyist(s)"
            ),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="date_free",
            field=models.CharField(blank=True, max_length=150, verbose_name="Date"),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="digitized_version",
            field=models.ForeignKey(
                blank=True,
                help_text="Exemples : Gallica, Photos personnelles [Stavros Lazaris], Biblioteca Apostolica Vaticana.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="vhsapp.digitizedversion",
                verbose_name="Source of the digitized version",
            ),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="manifest_final",
            field=models.BooleanField(
                default=False,
                help_text="<i style='color:#efb80b' class='fa-solid fa-triangle-exclamation'></i> ATTENTION : la version en cours de vérification ne peut plus être modifiée.",
                verbose_name="Validate annotations",
            ),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="miniaturists",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="Illuminator(s)"
            ),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="origin_place",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="Place of production"
            ),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="pinakes_link",
            field=models.URLField(blank=True, verbose_name="External link"),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="published",
            field=models.BooleanField(
                default=False,
                help_text="Les informations seront accessibles aux autres utilisateurs de la base.",
                verbose_name="Make public",
            ),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="reference_number",
            field=models.CharField(max_length=150, verbose_name="Shelfmark"),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="remarks",
            field=models.TextField(blank=True, verbose_name="Additional notes"),
        ),
        migrations.AlterField(
            model_name="manuscript",
            name="sheets",
            field=models.CharField(
                max_length=150, verbose_name="Number of folios/pages"
            ),
        ),
        migrations.AlterField(
            model_name="printed",
            name="author",
            field=models.ForeignKey(
                help_text="<ul><li>Indiquez [Anonyme] si auteur non identifié.</li><li>Si nom auteur non trouvé, merci de chercher directement dans <a href='https://data.bnf.fr/' target='_blank'>Data BnF</a>.</li></ul>",
                max_length=200,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="vhsapp.author",
                verbose_name="Auteurs et/ou Éditeurs scientifiques",
            ),
        ),
        migrations.AlterField(
            model_name="volume",
            name="manifest_final",
            field=models.BooleanField(
                default=False,
                help_text="<i style='color:#efb80b' class='fa-solid fa-triangle-exclamation'></i> ATTENTION : la version en cours de vérification ne peut plus être modifiée.",
                verbose_name="Valider les annotations",
            ),
        ),
    ]
