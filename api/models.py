from django.db import models

DAYS_OF_WEEK = (
    ("0", "MONDAY"),
    ("1", "TUESDAY"),
    ("2", "WEDNESDAY"),
    ("3", "THURSDAY"),
    ("4", "FRIDAY"),
    ("5", "SATURDAY"),
    ("6", "SUNDAY"),
)


class Store(models.Model):
    store_id = models.IntegerField(unique=True)
    inserted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Status(models.Model):
    STORE_STATUS = (
        ("active", "ACTIVE"),
        ("inactive", "INACTIVE"),
    )
    store = models.ForeignKey(to=Store, on_delete=models.DO_NOTHING)
    day_of_week = models.CharField(choices=DAYS_OF_WEEK, max_length=10)
    status = models.CharField(max_length=10, choices=STORE_STATUS)
    timestamp_utc = models.DateTimeField()

    inserted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BusinessHours(models.Model):
    store = models.ForeignKey(to=Store, on_delete=models.DO_NOTHING)
    day_of_week = models.CharField(choices=DAYS_OF_WEEK, max_length=10)
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    inserted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Timezone(models.Model):
    store = models.ForeignKey(to=Store, on_delete=models.DO_NOTHING)
    timezone = models.CharField(max_length=100)

    inserted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
