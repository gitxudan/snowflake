
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='view') }}

with odd_data as (

select id
    from {{ source('dbt_test', 'simple') }}
where id % 2 != 0  -- Filters for odd numbers
   or id is null   -- Keeps the null record if you want it included
)


select *
from odd_data

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null