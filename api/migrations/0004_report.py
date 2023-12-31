# Generated by Django 4.2.4 on 2023-08-03 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_results', '0011_taskresult_periodic_task_name'),
        ('api', '0003_remove_status_day_of_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uptime_last_hour', models.DateTimeField()),
                ('uptime_last_day', models.DateTimeField()),
                ('update_last_week', models.DateTimeField()),
                ('downtime_last_hour', models.DateTimeField()),
                ('downtime_last_day', models.DateTimeField()),
                ('downtime_last_week', models.DateTimeField()),
                ('inserted_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.store')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='django_celery_results.taskresult')),
            ],
        ),
    ]
