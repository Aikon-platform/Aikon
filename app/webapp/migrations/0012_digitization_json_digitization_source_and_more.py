# Generated by Django 4.0.4 on 2024-10-17 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0011_digitization_source_regions_json_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="digitization",
            name="json",
            field=models.JSONField(
                blank=True, null=True, verbose_name="JSON representation"
            ),
        ),
        migrations.AddField(
            model_name="digitization",
            name="source",
            field=models.ForeignKey(
                blank=True,
                help_text="Exemple : Gallica.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="webapp.digitizationsource",
                verbose_name="Source de la numérisation",
            ),
        ),
        migrations.AlterField(
            model_name="treatment",
            name="notify_email",
            field=models.BooleanField(
                blank=True,
                default=True,
                help_text="Envoyer un email lorsque la tâche est terminée",
                verbose_name="Notifier par email",
            ),
        ),
        migrations.AlterField(
            model_name="treatment",
            name="task_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("regions", "Extraction de régions d'images"),
                    ("similarity", "Calcul de score de similarité"),
                ],
                max_length=50,
                null=True,
                verbose_name="Type de tâche",
            ),
        ),
    ]
