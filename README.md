# Report API

The api consists of two endpoints

- trigger_report/ : which takes no input and returns the `report_id` as response
- get_report/ : which takes `report_id` as input and returns
    - status as running if the task is running
    - report csv file if the task is completed

## Generating Report
- When the `trigger_report/` endpoint is hit a new task is created and pushed into celery and the task id is returned.
- A celery worker picks up this task and starts executing the task.
- A table `TaskResults` manages all the states of the task.

## Calculating report fields
- Store, timezone, business hours and status (between current date and last week) data are loaded into polars dataframe. This is done to reduce the number of times we have to query the database and manage all the data wrangling task inside worker.

- First status timestamp and business hours' start and end time got for that working day are converted to relative timezones and are compared to see if the entry in the status is between the working hours of that store, and if the status is `active` we add it to the uptime and if it is `inactive` we add it to downtime, we do this to calculate each uptime_last_hour,uptime_last_day,uptime_last_week,downtime_last_hour,downtime_last_day,downtime_last_week