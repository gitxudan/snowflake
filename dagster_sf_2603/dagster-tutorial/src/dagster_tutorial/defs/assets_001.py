import dagster as dg
from dagster_aws import s3
from dagster_aws.s3 import S3Resource
import pandas as pd
from dagster_snowflake import SnowflakeResource
from snowflake.connector.pandas_tools import write_pandas
import os


@dg.asset
def customers() -> str:
    return "https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_customers.csv"


@dg.asset
def orders() -> str:
    return "https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_orders.csv"


@dg.asset
def sf_payments(snowflake: SnowflakeResource) -> str:
    # This is the URL you had originally   
    url = "https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/refs/heads/main/seeds/raw_payments.csv"
    
    # Now we actually pull the data into a DataFrame
    df = pd.read_csv(url)
    with snowflake.get_connection() as conn:
        write_pandas(conn = conn, 
                     df = df, 
                     table_name = "payments_asset_url", 
                     auto_create_table=True,
                     overwrite=True)
    return "payments is successfully loaded to Snowflake"

@dg.asset
def load_s3_to_snowflake(
    context:dg.AssetExecutionContext,
    s3: S3Resource,
    snowflake: SnowflakeResource
):
    # 1. Connect to S3 and get the object
    copy_query = f"""
        COPY INTO ORDERS_RAW
        FROM 's3://snowflake-2603/dagster_demo/orders.csv'
        CREDENTIALS = (
            AWS_KEY_ID='{s3.aws_access_key_id}'
            AWS_SECRET_KEY='{s3.aws_secret_access_key}'
        )
        FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1, DATE_FORMAT = 'YYYY/MM/DD')
    """

    with snowflake.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(copy_query)
            context.log.info("Data loaded from S3 to Snowflake successfully!")
    return "Data loaded from S3 to Snowflake successfully!"


class S3IngestionConfig(dg.Config):
    s3_key: str
    bucket: str
    last_modified: str  # The timestamp passed from the sensor

@dg.asset
def s3_to_snowflake(context, config: S3IngestionConfig,  snowflake: SnowflakeResource):
    """
    Metadata-driven ingestion asset that targets a specific S3 file.
    """
    # 1. Construct the specific S3 path
    s3_path = f"s3://{config.bucket}/{config.s3_key}"
    
    # 2. Log metadata for Observability
    context.log.info(
        f"Processing file: {config.s3_key} "
        f"with timestamp: {config.last_modified}"
    )

    # 3. Execute the Snowflake COPY INTO
    # Using 'idempotent' loading patterns typical of Senior DE workflows
    copy_query = f"""
        COPY INTO CUSTOMERS_RAW
        FROM '{s3_path}'
        credentials = (aws_key_id = {s3.aws_access_key_id}, aws_secret_key={s3.aws_secret_access_key})
        FILE_FORMAT = (TYPE = 'csv' FIELD_DELIMITER = ',' SKIP_HEADER = 1)
        ON_ERROR = 'ABORT_STATEMENT';
    """
    
    with snowflake.get_connection() as conn:
        conn.cursor().execute(copy_query)
        
    context.log.info(f"Successfully finalized load for {config.s3_key}")

