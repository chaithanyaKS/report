# Generated by Django 4.2.4 on 2023-08-03 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='store_id',
        ),
    ]
