-- models/metricflow_time_spine.sql
with days as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2009-01-01' as date)",
        end_date="cast('2012-01-01' as date)"
    )
    }}
)
select
    cast(date_day as date) as date_day
from days