{% snapshot scd2_customer_history %}

{{
    config(
      target_schema='snapshots',
      unique_key='id',
      strategy='check',
      check_cols=['age', 'name'],
    )
}}

-- This is the "Source" query that dbt will monitor for changes
select * from landing.raw_customer

{% endsnapshot %}