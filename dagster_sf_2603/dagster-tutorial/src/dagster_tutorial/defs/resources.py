import dagster as dg
from dagster import EnvVar
from dagster_snowflake import SnowflakeResource
from dagster_aws.s3 import S3Resource




snowflake = SnowflakeResource(
    account="xf67512.ap-southeast-1",
    user="tobbias",
    password="Password_12345",
    database="SF2603",
    schema="dbt_test",
    warehouse="COMPUTE_WH",
    role="ACCOUNTADMIN"
)

from dagster_aws.s3 import S3Resource
from dagster import EnvVar

s3_resource= S3Resource(
    aws_access_key_id=EnvVar("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=EnvVar("AWS_SECRET_ACCESS_KEY"),
    region_name="ap-southeast-2"
)

