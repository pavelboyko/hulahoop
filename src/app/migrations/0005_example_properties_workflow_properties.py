# Generated by Django 4.0.4 on 2022-05-22 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_loop_example_workflow'),
    ]

    operations = [
        migrations.AddField(
            model_name='example',
            name='properties',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='workflow',
            name='properties',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]
