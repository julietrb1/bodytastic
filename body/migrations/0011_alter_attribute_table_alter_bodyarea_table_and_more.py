# Generated by Django 4.0.3 on 2022-03-10 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('body', '0010_alter_report_unique_together'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='attribute',
            table='attribute',
        ),
        migrations.AlterModelTable(
            name='bodyarea',
            table='bodyarea',
        ),
        migrations.AlterModelTable(
            name='bodyimage',
            table='bodyimage',
        ),
        migrations.AlterModelTable(
            name='entry',
            table='entry',
        ),
        migrations.AlterModelTable(
            name='report',
            table='report',
        ),
        migrations.AlterModelTable(
            name='sensation',
            table='sensation',
        ),
    ]