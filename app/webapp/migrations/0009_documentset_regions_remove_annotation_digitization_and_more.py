# Generated by Django 4.0.4 on 2024-08-02 13:54

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("webapp", "0008_treatment_delete_apitask"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentSet",
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
                ("title", models.CharField(max_length=50)),
                ("is_public", models.BooleanField(default=False)),
                (
                    "wit_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(),
                        blank=True,
                        default=list,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "ser_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(),
                        blank=True,
                        default=list,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "digit_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(),
                        blank=True,
                        default=list,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "work_ids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(),
                        blank=True,
                        default=list,
                        null=True,
                        size=None,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "verbose_name": "Panier de documents",
                "verbose_name_plural": "Panier de documentss",
            },
        ),
        migrations.RenameField(
            model_name="regionpair",
            old_name="anno_ref_1",
            new_name="regions_id_1",
        ),
        migrations.RenameField(
            model_name="regionpair",
            old_name="anno_ref_2",
            new_name="regions_id_2",
        ),
        migrations.RemoveField(
            model_name="treatment",
            name="treated_object",
        ),
        migrations.RemoveField(
            model_name="treatment",
            name="treatment_type",
        ),
        migrations.RemoveField(
            model_name="treatment",
            name="user_id",
        ),
        migrations.AddField(
            model_name="regionpair",
            name="is_manual",
            field=models.BooleanField(default=False, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="regionpair",
            name="score",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="treatment",
            name="api_tracking_id",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name="treatment",
            name="is_finished",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name="treatment",
            name="notify_email",
            field=models.BooleanField(
                blank=True,
                default=True,
                help_text="Send an email when the task is finished",
                verbose_name="Notify by email",
            ),
        ),
        migrations.AddField(
            model_name="treatment",
            name="requested_by",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="treatment",
            name="requested_on",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="treatment",
            name="treated_objects",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="content",
            name="work",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contents",
                to="webapp.work",
                verbose_name="Œuvre",
            ),
        ),
        migrations.AlterField(
            model_name="regionpair",
            name="category",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="regionpair",
            name="category_x",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), default=list, null=True, size=None
            ),
        ),
        migrations.AlterField(
            model_name="treatment",
            name="status",
            field=models.CharField(
                choices=[
                    ("CANCELLED", "CANCELLED"),
                    ("ERROR", "ERROR"),
                    ("IN PROGRESS", "IN PROGRESS"),
                    ("PENDING", "PENDING"),
                    ("STARTED", "STARTED"),
                    ("SUCCESS", "SUCCESS"),
                ],
                default="PENDING",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="treatment",
            name="task_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("regions", "regions"),
                    ("vectorization", "vectorization"),
                    ("similarity", "similarity"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddIndex(
            model_name="regionpair",
            index=models.Index(fields=["img_1"], name="webapp_regi_img_1_637fec_idx"),
        ),
        migrations.AddIndex(
            model_name="regionpair",
            index=models.Index(fields=["img_2"], name="webapp_regi_img_2_ec71b6_idx"),
        ),
        migrations.AddIndex(
            model_name="regionpair",
            index=models.Index(
                fields=["regions_id_1"], name="webapp_regi_regions_23ea83_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="regionpair",
            index=models.Index(
                fields=["regions_id_2"], name="webapp_regi_regions_8f0f96_idx"
            ),
        ),
        migrations.AddField(
            model_name="documentset",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="treatment",
            name="document_set",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="treatments",
                to="webapp.documentset",
                verbose_name="Sélection de documents",
            ),
        ),
        # migrations.CreateModel(
        #     name='Regions',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('model', models.CharField(max_length=150)),
        #         ('is_validated', models.BooleanField(default=False)),
        #     ],
        #     options={
        #         'verbose_name': 'Régions',
        #         'verbose_name_plural': 'Régions',
        #     },
        # ),
        # migrations.RemoveField(
        #     model_name='annotation',
        #     name='digitization',
        # ),
        # migrations.DeleteModel(
        #     name='Annotation',
        # ),
        # migrations.AddField(
        #     model_name='regions',
        #     name='digitization',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='regions', to='webapp.digitization', verbose_name='Numérisation'),
        # ),
        migrations.RenameModel(
            old_name="Annotation",
            new_name="Regions",
        ),
        migrations.AlterModelOptions(
            name="regions",
            options={
                "verbose_name": "Régions",
                "verbose_name_plural": "Régions",
            },
        ),
        migrations.AlterField(
            model_name="regions",
            name="digitization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="regions",
                to="webapp.digitization",
                verbose_name="Numérisation",
            ),
        ),
    ]