from django.contrib.postgres.fields import ArrayField
from django.db import models, connection
from app.webapp.models.utils.functions import get_fieldname


def get_name(fieldname, plural=False):
    fields = {
        "RegionPair": {
            "en": "region pair",
            "fr": "paire de régions",
        },
    }
    return get_fieldname(fieldname, fields, plural)


class RegionPairManager(models.Manager):
    def bulk_update_or_create(self, objs, update_fields, match_field, update_field):
        if not objs:
            return

        model = self.model
        fields = [
            f
            for f in model._meta.fields
            if f.name in update_fields or f.name in match_field
        ]

        with connection.cursor() as cursor:
            table_name = model._meta.db_table
            columns = ", ".join(f.column for f in fields)
            placeholders = ", ".join("%s" for _ in fields)

            conflict_update = ", ".join(
                f"{f.column} = EXCLUDED.{f.column}"
                for f in fields
                if f.name in update_fields and f.name != update_field
            )

            if conflict_update:
                conflict_update += ", "
            conflict_update += f"{update_field} = CASE WHEN EXCLUDED.{update_field} > {table_name}.{update_field} THEN EXCLUDED.{update_field} ELSE {table_name}.{update_field} END"

            sql = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders})
                ON CONFLICT ({', '.join(f.column for f in fields if f.name in match_field)})
                DO UPDATE SET {conflict_update}
            """

            data = [[getattr(obj, f.name) for f in fields] for obj in objs]

            cursor.executemany(sql, data)


class RegionPair(models.Model):
    class Meta:
        verbose_name = get_name("RegionPair")
        verbose_name_plural = get_name("RegionPair", True)
        app_label = "webapp"
        constraints = [
            models.UniqueConstraint(fields=["img_1", "img_2"], name="unique_img_pair")
        ]
        # make database queries on those fields more efficient
        indexes = [
            models.Index(fields=["img_1"]),
            models.Index(fields=["img_2"]),
            models.Index(fields=["regions_id_1"]),
            models.Index(fields=["regions_id_2"]),
        ]

    def __str__(self):
        return f"{self.img_1} | {self.img_2}"

    img_1 = models.CharField(max_length=150)
    img_2 = models.CharField(max_length=150)
    regions_id_1 = models.CharField(max_length=150)
    regions_id_2 = models.CharField(max_length=150)

    """
    Score of similarity between the two regions (only from automatic pairs)
    """
    score = models.FloatField(blank=True, null=True)
    """
    Category of the similarity
    1 = exact match
    2 = partial match
    3 = semantic match
    4 = no match
    """
    category = models.IntegerField(blank=True, null=True)
    """
    List of users Ids that have added this pair to their "user category" list
    """
    category_x = ArrayField(models.IntegerField(), null=True, default=list)
    """
    Is this pair manually added by a user or automatically generated (ie from a score file)
    """
    is_manual = models.CharField(max_length=150, null=True)

    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    objects = RegionPairManager()
