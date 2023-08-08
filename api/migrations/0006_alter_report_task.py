# Generated by Django 4.2.4 on 2023-08-08 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_results', '0011_taskresult_periodic_task_name'),
        ('api', '0005_remove_report_downtime_last_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='django_celery_results.taskresult', to_field='task_id'),
        ),
    ]
