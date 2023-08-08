# Generated by Django 4.2.4 on 2023-08-08 10:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_report_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(upload_to='csvs', validators=[django.core.validators.FileExtensionValidator(['csv'])]),
        ),
    ]