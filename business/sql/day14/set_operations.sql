CREATE OR REPLACE TEMP VIEW app_users AS
SELECT * FROM VALUES
    (101, 'Alice', '2026-01-01'),
    (102, 'Bob',   '2026-01-02'),
    (103, 'Cindy', '2026-01-03'),
    (104, 'David', '2026-01-04')
AS app_users(user_id, user_name, signup_date);


CREATE OR REPLACE TEMP VIEW web_users AS
SELECT * FROM VALUES
    (103, 'Cindy', '2026-01-03'),
    (104, 'David', '2026-01-04'),
    (105, 'Emma',  '2026-01-05'),
    (106, 'Frank', '2026-01-06')
AS web_users(user_id, user_name, signup_date);

select user_id,
       user_name,
       signup_date
from app_users
union
select user_id,
       user_name,
       signup_date
from web_users
;

select user_id,
       user_name
from app_users
except
select user_id,
       user_name
from web_users
;

with all_users as(
    select user_id,
           user_name,
           'app' as source
    from app_users
    union all
    select user_id,
           user_name,
           'web' as source
    from web_users
)
select user_id,
       user_name,
       case
        when count('*') > 1 then 'both'
        else first(source)
       end as source
from all_users
group by user_id,user_name
;

