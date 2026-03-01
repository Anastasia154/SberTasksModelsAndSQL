
create table users
	(
		id integer primary key
		, username varchar not null
		, created_at date not null
	);

create table user_activity
	(
		id integer primary key
		, user_id integer not null
		, activity_type_id integer not null
		, activity_date date not null
		, foreign key (user_id) references users(id)
	);

create table activity_types
	(
		id integer primary key
		, name varchar not null
	);

create table user_roles
	(
		id integer primary key
		, user_id integer not null
		, role varchar not null
		, assigned_at date not null
		, foreign key (user_id) references users(id)
	);



insert into users (id, username, created_at) values
	(1, 'user1', '2024-01-01')
	, (2, 'user2', '2024-02-15')
	, (3, 'user3', '2024-03-10')
	, (4, 'user4', '2024-04-01')
	, (5, 'user5', '2024-05-01')
	, (6, 'user6', '2024-06-01');

insert into activity_types (id, name) values
	(1, 'login')
	, (2, 'logout')
	, (3, 'purchase');

insert into user_activity (id, user_id, activity_type_id, activity_date) values
	(1, 1, 1, '2024-10-01')
	, (2, 1, 2, '2024-10-05')
	, (3, 1, 1, '2024-10-10')
	, (4, 2, 1, '2024-10-15')
	, (5, 2, 3, '2024-09-20')
	, (6, 3, 1, '2024-08-25')
	, (7, 4, 1, '2024-10-22')
	, (8, 4, 2, '2024-10-25')
	, (9, 6, 1, '2024-10-05')
	, (10, 6, 3, '2024-10-10')
	, (11, 6, 1, '2024-09-30');

insert into user_roles (id, user_id, role, assigned_at) values
	(1, 1, 'admin', '2024-10-01')
	, (2, 1, 'moderator', '2024-10-05')
	, (3, 2, 'user', '2024-10-10')
	, (4, 4, 'guest', '2024-10-20')
	, (5, 6, 'editor', '2024-10-15');


SELECT 
    u.id,
    u.username,
    u.created_at,
    GROUP_CONCAT(DISTINCT ur.role) AS roles,
    COUNT(ua.id) AS activity_count_last_month
FROM 
    users u
LEFT JOIN 
    user_roles ur ON u.id = ur.user_id
LEFT JOIN 
    user_activity ua ON u.id = ua.user_id 
    AND ua.activity_date >= date('now', '-1 month')
GROUP BY 
    u.id, u.username, u.created_at
ORDER BY 
    activity_count_last_month DESC;
	
-- Результат --
-- 1|user1|2024-01-01|admin,moderator|0
-- 2|user2|2024-02-15|user|0
-- 3|user3|2024-03-10||0
-- 4|user4|2024-04-01|guest|0
-- 5|user5|2024-05-01||0
-- 6|user6|2024-06-01|editor|0