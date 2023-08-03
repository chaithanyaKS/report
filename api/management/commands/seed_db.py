import csv
import itertools
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from api.models import BusinessHours, Status, Store, Timezone


class Command(BaseCommand):
    help = "Seed the database tables with data stored in data folder"

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO(f"Seeding Store Table Started"))
        self.populate_store_table()
        self.stdout.write(self.style.SUCCESS(f"Seeding Store Table Finished"))

        self.stdout.write(
            self.style.HTTP_INFO(f"\nSeeding BusinessHours Table Started")
        )
        self.populate_business_hours()
        self.stdout.write(self.style.SUCCESS(f"Seeding Business Table Finished"))

        self.stdout.write(self.style.HTTP_INFO(f"\nSeeding Status Table Started"))
        self.populate_status_table()
        self.stdout.write(self.style.SUCCESS(f"Seeding Status Table Finished"))

        self.stdout.write(self.style.HTTP_INFO(f"\nSeeding Timezone Table Started"))
        self.populate_timezone_table()
        self.stdout.write(self.style.SUCCESS(f"Seeding Timezone Table Finished"))
        self.stdout.write(self.style.SUCCESS("\nSeeding Database Completed!"))

    def read_csv(self, filename: str):
        with open(filename, "r") as fp:
            reader = csv.DictReader(fp, delimiter=",")
            for row in reader:
                yield row

    def populate_store_table(self):
        unique_ids = set()
        id_iterable = itertools.chain(
            self.read_csv("data/timezone.csv"),
            self.read_csv("data/status.csv"),
            self.read_csv("data/business_hours.csv"),
        )
        unique_ids.update((row["store_id"] for row in id_iterable))

        Store.objects.bulk_create((Store(id=id) for id in unique_ids))
        self.stdout.write(self.style.HTTP_INFO(f"Seeded {Store.objects.count()} items"))

    def populate_business_hours(self):
        BusinessHours.objects.bulk_create(
            (
                BusinessHours(
                    store_id=row["store_id"],
                    day_of_week=row["day"],
                    start_time_local=row["start_time_local"],
                    end_time_local=row["end_time_local"],
                )
                for row in self.read_csv("data/business_hours.csv")
            )
        )

        self.stdout.write(
            self.style.HTTP_INFO(f"Seeded {BusinessHours.objects.count()} items")
        )

    def populate_status_table(self):
        Status.objects.bulk_create(
            (
                Status(
                    store_id=row["store_id"],
                    status=row["status"],
                    timestamp_utc=self.format_datetime_str(row["timestamp_utc"]),
                )
                for row in self.read_csv("data/status.csv")
            )
        )

        self.stdout.write(
            self.style.HTTP_INFO(f"Seeded {Status.objects.count()} items")
        )

    def populate_timezone_table(self):
        Timezone.objects.bulk_create(
            (
                Timezone(
                    store_id=row["store_id"],
                    timezone=row["timezone_str"],
                )
                for row in self.read_csv("data/timezone.csv")
            )
        )

        self.stdout.write(
            self.style.HTTP_INFO(f"Seeded {Timezone.objects.count()} items")
        )

    def format_datetime_str(self, date_str: str) -> str:
        datetime_object = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f %Z")
        return datetime_object.strftime("%Y-%m-%d %H:%M:%S.%f+00:00")
