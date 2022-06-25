# Generated by Django 4.0.4 on 2022-06-25 15:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_issue_fingerprint_alter_issue_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='example',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True),
        ),
    ]
