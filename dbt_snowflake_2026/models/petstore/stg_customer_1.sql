{{
  config(
    materialized='incremental',
    unique_key='id',
    incremental_strategy='merge'
  )
}}

select 
    * from landing.raw_customer

{% if is_incremental() %}
  -- This filter ensures we only grab rows that arrived after the last run
  -- Replace 'loaded_at' with your actual timestamp column
  where _ingestion_at > (select max(_ingestion_at) from {{ this }})
{% endif %}