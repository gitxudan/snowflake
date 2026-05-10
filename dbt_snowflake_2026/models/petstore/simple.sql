/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/


{{ config(materialized = 'table') }}

with source_data as (

    {% for i in range(1, 21) %}
    select {{ i }} as id
    union all
    {% endfor %}
    select null as id
)

select *
from source_data

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null