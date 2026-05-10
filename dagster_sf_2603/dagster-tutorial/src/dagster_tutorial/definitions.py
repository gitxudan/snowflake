from pathlib import Path
from dagster import Definitions, load_assets_from_modules, resources
from .defs import assets_001
from dagster_tutorial.defs.resources import s3_resource, snowflake
from .defs.schedules import daily_schedule
from .defs.sensors import my_job,s3_file_sensor

all_assets = load_assets_from_modules([assets_001])

defs = Definitions(
    assets=all_assets,
    schedules=[daily_schedule],
    jobs=[my_job],
    sensors=[s3_file_sensor],
    resources={
        "snowflake": snowflake,
        "s3": s3_resource,
    },
)
