# Generated by Django 4.0.4 on 2022-06-16 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_exampletag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='example',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='tags',
        ),
    ]