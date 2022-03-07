# Generated by Django 4.0.3 on 2022-03-07 01:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def seed_attributes(apps, _):
    """Inserts default sensations that the app should start with."""
    Attribute = apps.get_model("body.Attribute")
    attributes = (
        "After exercise",
        "After big meal",
        "Feeling bloated",
    )

    Attribute.objects.bulk_create([Attribute(name=name) for name in attributes])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("body", "0008_rename_bodyareaentry_entry_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attribute",
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
                ("name", models.CharField(max_length=50)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="report",
            name="attributes",
            field=models.ManyToManyField(blank=True, to="body.attribute"),
        ),
        migrations.RunPython(seed_attributes, migrations.RunPython.noop),
    ]
