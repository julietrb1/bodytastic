# Generated by Django 4.0.3 on 2022-03-13 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('body', '0001_squashed_0011_alter_attribute_table_alter_bodyarea_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='default_consumption_quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
