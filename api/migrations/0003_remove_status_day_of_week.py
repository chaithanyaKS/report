# Generated by Django 4.2.4 on 2023-08-03 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_store_store_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='day_of_week',
        ),
    ]
