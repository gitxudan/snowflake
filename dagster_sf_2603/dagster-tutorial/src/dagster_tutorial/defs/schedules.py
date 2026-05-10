import dagster as dg
from .assets_001 import sf_payments


daily_schedule = dg.ScheduleDefinition(
    name="job_sf_payments",
    cron_schedule="* * * * *",
    #target=daily_job,
    target=[sf_payments]
)
