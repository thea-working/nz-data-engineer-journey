CREATE OR REPLACE TEMP VIEW user_profile_updates AS
SELECT * FROM VALUES
    (1, 'Alice', 'Beijing',  '2026-01-01 09:00:00'),
    (1, 'Alice', 'Shanghai', '2026-01-05 10:00:00'),
    (1, 'Alice', 'Shenzhen', '2026-01-08 15:00:00'),

    (2, 'Bob', 'Beijing', '2026-01-02 11:00:00'),
    (2, 'Bob', 'Guangzhou', '2026-01-06 14:00:00'),

    (3, 'Cindy', 'Shanghai', '2026-01-03 08:00:00')
AS user_profile_updates(user_id, name, city, updated_at);
-- Q1 : 每个用户只保留最新的一条 profile 记录。
select user_id,
       name,
       city,
       updated_at
from (
        select user_id,
               name,
               city,
               updated_at,
               row_number() over(
                partition by user_id
                order by updated_at desc
               ) as row_num
        from user_profile_updates
) user_profile
where row_num = 1
;
--1	Alice	Shenzhen	2026-01-08 15:00:00
--2	Bob	Guangzhou	2026-01-06 14:00:00
--3	Cindy	Shanghai	2026-01-03 08:00:00

CREATE OR REPLACE TEMP VIEW user_profile_updates AS
SELECT * FROM VALUES
    (1, 'Alice', 'Beijing',  '2026-01-01 09:00:00'),
    (1, 'Alice', 'Shanghai', '2026-01-05 10:00:00'),
    (1, 'Alice', 'Shenzhen', '2026-01-08 15:00:00'),

    (2, 'Bob', 'Beijing',    '2026-01-02 11:00:00'),
    (2, 'Bob', 'Guangzhou',  '2026-01-06 14:00:00'),
    (2, 'Bob', 'Shanghai',   '2026-01-06 14:00:00'),

    (3, 'Cindy', 'Shanghai', '2026-01-03 08:00:00')
AS user_profile_updates(user_id, name, city, updated_at);
-- Q2: 每个用户保留所有“最新时间”的记录。
select user_id,
       name,
       city,
       updated_at
from (
        select user_id,
               name,
               city,
               updated_at,
               rank() over(
                partition by user_id
                order by updated_at desc
               ) as rank
        from user_profile_updates
) user_profile
where rank = 1
;
--1	Alice	Shenzhen	2026-01-08 15:00:00
--2	Bob	Guangzhou	2026-01-06 14:00:00
--2	Bob	Shanghai	2026-01-06 14:00:00
--3	Cindy	Shanghai	2026-01-03 08:00:00

CREATE OR REPLACE TEMP VIEW user_events AS
SELECT * FROM VALUES
    (1, 'Alice', '2026-01-01 09:00:00', 'login'),
    (1, 'Alice', '2026-01-01 09:10:00', 'view'),
    (1, 'Alice', '2026-01-01 09:30:00', 'purchase'),
    (1, 'Alice', '2026-01-01 10:00:00', 'logout'),
    (1, 'Alice', '2026-01-01 10:45:00', 'login'),

    (2, 'Bob', '2026-01-01 09:05:00', 'login'),
    (2, 'Bob', '2026-01-01 09:20:00', 'view'),
    (2, 'Bob', '2026-01-01 09:45:00', 'logout'),

    (3, 'Cindy', '2026-01-01 10:00:00', 'login'),
    (3, 'Cindy', '2026-01-01 10:15:00', 'view')
AS user_events(user_id, name, event_time, event_type);

-- Q3: 识别新的 Session
select user_id,
       name,
       event_time,
       event_type,
       previous_event_time,
       case when previous_event_time is null
            or timestampdiff(MINUTE,previous_event_time,event_time) > 30
            then 1
            else 0
            end as is_new_session
from (
        select user_id,
               name,
               event_time,
               event_type,
               lag(event_time) over(
                partition by user_id
                order by event_time
               ) as previous_event_time
        from user_events
) user_riched_user_events
;
--1	Alice	2026-01-01 09:00:00	login	NULL	1
--1	Alice	2026-01-01 09:10:00	view	2026-01-01 09:00:00	0
--1	Alice	2026-01-01 09:30:00	purchase	2026-01-01 09:10:00	0
--1	Alice	2026-01-01 10:00:00	logout	2026-01-01 09:30:00	0
--1	Alice	2026-01-01 10:45:00	login	2026-01-01 10:00:00	1
--2	Bob	2026-01-01 09:05:00	login	NULL	1
--2	Bob	2026-01-01 09:20:00	view	2026-01-01 09:05:00	0
--2	Bob	2026-01-01 09:45:00	logout	2026-01-01 09:20:00	0
--3	Cindy	2026-01-01 10:00:00	login	NULL	1
--3	Cindy	2026-01-01 10:15:00	view	2026-01-01 10:00:00	0

select user_id,
       name,
       event_time,
       event_type,
       previous_event_time,
       is_new_session,
       sum(is_new_session) over(
        partition by user_id
        order by event_time
        rows between unbounded preceding and current row
       ) as session_id
from (
        select user_id,
               name,
               event_time,
               event_type,
               previous_event_time,
               case when previous_event_time is null
                    or timestampdiff(MINUTE,previous_event_time,event_time) > 30
                    then 1
                    else 0
                    end as is_new_session
        from (
                select user_id,
                       name,
                       event_time,
                       event_type,
                       lag(event_time) over(
                        partition by user_id
                        order by event_time
                       ) as previous_event_time
                from user_events
        ) user_riched_user_events
) user_session_user_events
;
--1	Alice	2026-01-01 09:00:00	login	NULL	1	1
--1	Alice	2026-01-01 09:10:00	view	2026-01-01 09:00:00	0	1
--1	Alice	2026-01-01 09:30:00	purchase	2026-01-01 09:10:00	0	1
--1	Alice	2026-01-01 10:00:00	logout	2026-01-01 09:30:00	0	1
--1	Alice	2026-01-01 10:45:00	login	2026-01-01 10:00:00	1	2
--2	Bob	2026-01-01 09:05:00	login	NULL	1	1
--2	Bob	2026-01-01 09:20:00	view	2026-01-01 09:05:00	0	1
--2	Bob	2026-01-01 09:45:00	logout	2026-01-01 09:20:00	0	1
--3	Cindy	2026-01-01 10:00:00	login	NULL	1	1
--3	Cindy	2026-01-01 10:15:00	view	2026-01-01 10:00:00	0	1