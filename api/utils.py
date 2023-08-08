from datetime import datetime, time, timedelta

CURRENT_DATE = datetime(2023, 1, 25)
LAST_HOUR = CURRENT_DATE - timedelta(hours=1)
LAST_DAY = CURRENT_DATE - timedelta(days=1)
LAST_WEEK = CURRENT_DATE - timedelta(days=7)

business_hour = (datetime(2023, 1, 24, 9), datetime(2023, 1, 24, 12))


# def get_last_hour(
#     business_hours: tuple[datetime, datetime],
#     current_time: datetime,
# ) -> datetime:
#     if current_time - business_hour[0] < timedelta(minutes=30):
#         pass
