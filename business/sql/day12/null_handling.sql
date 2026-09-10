CREATE OR REPLACE TEMP VIEW customer_payments AS
SELECT * FROM VALUES
    (1, 101, '2026-01-01', 100, 'paid'),
    (2, 101, '2026-01-05', NULL, 'paid'),
    (3, 101, '2026-01-10', 200, 'refunded'),

    (4, 102, '2026-01-03', 300, 'paid'),
    (5, 102, '2026-01-08', NULL, 'pending'),

    (6, 103, '2026-01-02', NULL, 'pending'),
    (7, 103, '2026-01-15', 500, 'paid'),

    (8, 104, '2026-01-04', NULL, 'refunded'),
    (9, 104, '2026-01-20', NULL, 'pending')
AS customer_payments(
    payment_id,
    customer_id,
    payment_date,
    amount,
    status
);

select customer_id,
       count(payment_id) as total_payments,
       count(amount) as payments_with_amount,
       sum(amount) as total_amount,
       avg(amount) as avg_amount
from customer_payments
group by customer_id
;

select customer_id,
       coalesce(sum(amount), 0) as total_amount,
       coalesce(sum( case
                      when status = 'paid' then amount
                      else 0
                    end
       ), 0) as paid_amount,
       coalesce(sum( case
                      when status = 'refunded' then amount
                      else 0
                    end
       ), 0) as refunded_amount
from customer_payments
group by customer_id
;

with customer_agg_payments as (
    select customer_id,
           count(payment_id) as total_payments,
           sum(case when status = 'paid' then 1 else 0 end) as paid_payments,
           coalesce(sum( case
                          when status = 'paid' then amount
                          else 0
                        end
           ), 0) as paid_amount
    from customer_payments
    group by customer_id
    having count(payment_id) >= 2
)
select customer_id,
       total_payments,
       paid_payments,
       paid_amount
from customer_agg_payments
where paid_payments >= 1 and paid_amount >= 300
;