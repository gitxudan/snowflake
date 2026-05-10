-- This references the source you just defined
SELECT
    orderid as order_id,
    customerid as customer_id,
    orderdate as order_date,
    paymenttype as payment_method,
    totalprice as total_price,
    state as location_state
FROM landing.orders