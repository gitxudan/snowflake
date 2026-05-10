select *
from {{ ref('customers__1') }}
where age > 100