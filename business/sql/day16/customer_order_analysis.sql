CREATE OR REPLACE TEMP VIEW customers AS
SELECT * FROM VALUES
    (101, 'Alice'),
    (102, 'Bob'),
    (103, 'Cindy'),
    (104, 'David'),
    (105, 'Emma'),
    (106, 'Frank')
AS customers(customer_id, customer_name);

CREATE OR REPLACE TEMP VIEW orders AS
SELECT * FROM VALUES
    (1, 101, '2026-01-05', 100, 'completed'),
    (2, 101, '2026-01-10', 200, 'completed'),
    (3, 102, '2026-01-08', 300, 'completed'),
    (4, 103, '2026-01-12', 150, 'cancelled'),
    (5, 104, '2026-01-15', 500, 'completed'),
    (6, 105, '2026-01-18', 400, 'completed')
AS orders(order_id, customer_id, order_date, amount, status);

CREATE OR REPLACE TEMP VIEW payments AS
SELECT * FROM VALUES
    (1001, 1, 100, 'paid'),
    (1002, 2, 200, 'paid'),
    (1003, 3, 250, 'paid'),
    (1004, 5, 500, 'paid'),
    (1005, 6, 300, 'paid')
AS payments(payment_id, order_id, payment_amount, payment_status);

select c.customer_id as customer_id,
           c.customer_name as customer_name,
           count(order_id) as order_count,
           coalesce(sum(amount),0) as total_order_amount
from customers c
left join orders o
on c.customer_id = o.customer_id
group by c.customer_id, c.customer_name
;

select o.order_id,
       o.customer_id,
       o.amount,
       o.status
from orders o
left join payments p
on o.order_id = p.order_id
where p.payment_id is null
;

with payments_summary as (
    select order_id,
           sum(payment_amount) as total_payment
    from payments
    where payment_status = 'paid'
    group by order_id
)
select o.order_id,
       o.customer_id,
       o.amount,
       coalesce(ps.total_payment, 0) as total_payment,
       (o.amount - coalesce(ps.total_payment, 0)) as difference
from orders o
left join payments_summary ps
on o.order_id = ps.order_id
where o.status = 'completed'
and o.amount <> COALESCE(ps.total_payment, 0)
;
