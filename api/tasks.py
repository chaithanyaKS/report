from datetime import datetime, timedelta

import polars as pl
import pytz
from celery import current_task, shared_task
from django_celery_results.models import TaskResult

from api.models import Report

STATUS_FORMAT = "%Y-%m-%d %H:%M:%S%.f %Z"
BUSINESS_HOURS_FORMAT = "%H:%M:%S"


def get_status_data(
    status_df: pl.DataFrame, from_date: datetime, to_date: datetime, tz: str
):
    return (
        status_df.with_columns(pl.col("timestamp_utc").dt.replace_time_zone(tz))
        .filter(pl.col("timestamp_utc").is_between(to_date, from_date))
        .sort("timestamp_utc", descending=True)
    )


def get_business_hours(business_hours_df: pl.DataFrame, tz: str, day: int):
    b = (
        business_hours_df.with_columns(
            pl.col(["start_time_local", "end_time_local"]).dt.replace_time_zone(tz)
        )
        .filter(pl.col("day") == day)
        .select(pl.col(["start_time_local", "end_time_local"]))
    )
    if b.is_empty():
        ptz = pytz.timezone(tz)
        return (
            datetime(1, 1, 1, 0, tzinfo=ptz),
            datetime(1, 1, 1, 23, 59, 59, tzinfo=ptz),
        )
    else:
        return (b["start_time_local"][0], b["end_time_local"][0])


def get_uptime_downtime_last_hr(
    last_hr_status: pl.DataFrame,
    start_time: datetime,
    end_time: datetime,
    current_date: datetime,
):
    last_uptime_hr = timedelta(minutes=0)
    last_downtime_hr = timedelta(minutes=0)
    timestamp: datetime = last_hr_status["timestamp_utc"][0]
    status = last_hr_status["status"][0]

    if start_time.hour <= timestamp.hour <= end_time.hour and status == "active":
        last_uptime_hr = current_date - timestamp
    else:
        last_downtime_hr = current_date - timestamp

    return (
        last_uptime_hr.total_seconds() // 60,
        last_downtime_hr.total_seconds() // 60,
    )


def get_uptime_downtime_last_day(
    last_day_status: pl.DataFrame,
):
    last_uptime_day = timedelta(minutes=0)
    last_downtime_day = timedelta(minutes=0)

    for status, count in (
        last_day_status.drop("store_id").groupby("status").count().iter_rows()
    ):
        if status == "active":
            last_uptime_day += timedelta(hours=count)
        else:
            last_downtime_day += timedelta(hours=count)

    return (
        last_uptime_day.total_seconds() // 3600,
        last_downtime_day.total_seconds() // 3600,
    )


def get_uptime_downtime_last_week(
    last_week_status: pl.DataFrame,
):
    last_uptime_day = timedelta(minutes=0)
    last_downtime_day = timedelta(minutes=0)

    for status, count in (
        last_week_status.drop("store_id").groupby("status").count().iter_rows()
    ):
        if status == "active":
            last_uptime_day += timedelta(hours=count)
        else:
            last_downtime_day += timedelta(hours=count)

    return (
        last_uptime_day.total_seconds() // 3600,
        last_downtime_day.total_seconds() // 3600,
    )


@shared_task
def generate_report(current_date: datetime):
    last_week = current_date - timedelta(days=7)
    last_day = current_date - timedelta(days=1)
    connection_uri = "sqlite://./db.sqlite3"
    task_id = current_task.request.id
    file_name = f"./csvs/{task_id}_report.csv"

    store_timezone = pl.read_database(
        """ SELECT "api_store"."id", "api_timezone"."timezone"
            FROM "api_store" LEFT OUTER JOIN "api_timezone"
            ON ("api_timezone"."store_id" = "api_store"."id")""",
        connection=connection_uri,
        engine="connectorx",
    ).fill_null("America/Chicago")

    business_hours_df = (
        pl.read_database(
            ''' SELECT "api_businesshours"."store_id",
            "api_businesshours"."start_time_local",
            "api_businesshours"."end_time_local",
            "api_businesshours"."day_of_week" AS "day"
            FROM "api_businesshours"''',
            connection=connection_uri,
            engine="connectorx",
        )
        .with_columns(
            pl.col(["start_time_local", "end_time_local"])
            .dt.to_string(format=BUSINESS_HOURS_FORMAT)
            .str.to_datetime(format=BUSINESS_HOURS_FORMAT)
        )
        .with_columns(pl.col("day").cast(pl.UInt8))
    )

    status_df = pl.read_database(
        'SELECT "api_status"."store_id", "api_status"."status", "api_status"."timestamp_utc" FROM "api_status"',
        connection=connection_uri,
        engine="connectorx",
    )

    status_list = []
    for store_id, tz in store_timezone.iter_rows():
        status = status_df.filter(pl.col("store_id") == store_id)
        business_hrs = business_hours_df.filter(pl.col("store_id") == store_id)
        current_date = current_date.astimezone(pytz.timezone(tz))
        last_week = last_week.astimezone(pytz.timezone(tz))
        last_day = last_day.astimezone(pytz.timezone(tz))

        last_week_data = get_status_data(status, current_date, last_week, tz)
        if last_week_data.is_empty():
            continue
        (start_time, end_time) = get_business_hours(business_hrs, tz, 1)

        last_day_data = get_status_data(status, current_date, last_day, tz)

        (uptime_last_hour, downtime_last_hour) = get_uptime_downtime_last_hr(
            last_week_data[0], start_time, end_time, current_date
        )
        (uptime_last_day, downtime_last_day) = get_uptime_downtime_last_day(
            last_day_data
        )
        (uptime_last_week, downtime_last_week) = get_uptime_downtime_last_day(
            last_week_data
        )

        status_list.append(
            {
                "store_id": store_id,
                "uptime_last_hour": uptime_last_hour,
                "uptime_last_day": uptime_last_day,
                "uptime_last_week": uptime_last_week,
                "downtime_last_hour": downtime_last_hour,
                "downtime_last_day": downtime_last_day,
                "downtime_last_week": downtime_last_week,
            }
        )

    pl.DataFrame(status_list).write_csv(file_name, separator=",")
    Report.objects.create(task_id=task_id, file=f"{task_id}_report.csv")
