import dagster as dg
from datetime import datetime,timezone

from dagster_tutorial.defs.assets_001 import s3_to_snowflake

my_job = dg.define_asset_job("my_job", selection=[s3_to_snowflake])

@dg.sensor(
               job = my_job,
               minimum_interval_seconds=5,
               required_resource_keys={"s3"},
    default_status=dg.DefaultSensorStatus.RUNNING,)
def s3_file_sensor(context):
    
    s3 = context.resources.s3
    # Get last processed timestamp from cursor
    #last_mtime = datetime.fromisoformat(context.cursor) if context.cursor else datetime.min
    
    last_mtime = (
    datetime.fromisoformat(context.cursor)
    if context.cursor
    else datetime.min.replace(tzinfo=timezone.utc)
)
    
    max_mtime = last_mtime
    bucket = "snowflake-2603"
    prefix = "ext_stage/"

    # Use boto3 to list objects in the bucket
    paginator = s3.get_paginator("list_objects_v2")
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            file_mtime = obj["LastModified"]
            filename = obj["Key"]

            # Skip if not a new/updated file
            if file_mtime <= last_mtime:
                continue

            # yield RunRequest
            yield dg.RunRequest(
                run_key=f"{filename}:{file_mtime.timestamp()}",
                run_config={
                    "ops": {
                        "s3_to_snowflake": {
                            "config": {"s3_key": filename, "bucket": bucket, "last_modified": file_mtime.isoformat() }
                        }
                    }
                }
            )
            yield dg.RunRequest(
                run_key=f"{filename}:{file_mtime.timestamp()}",
                run_config={
                    "assets": {  # <--- Changed from "ops" to "assets"
                        "s3_to_snowflake": {
                "config": {
                    "s3_key": filename, 
                    "bucket": bucket, 
                    "last_modified": file_mtime.isoformat() 
                }
            }
        }
    }
    
)
            if file_mtime > max_mtime:
                max_mtime = file_mtime

    # Update cursor with the latest ISO timestamp
    context.update_cursor(max_mtime.isoformat())