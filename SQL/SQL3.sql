create table clients
	(
		client_id serial primary key
		, name varchar(100) not null
		, age integer check (age >= 0)
		, registration_date date not null
	);

create table accounts
	(
		account_id serial primary key
		, client_id integer references clients(client_id) on delete cascade
		, balance decimal(15, 2) not null check (balance >= 0)
		, open_date date not null
	);

create table transactions
	(
		transaction_id serial primary key
		, account_id integer references accounts(account_id) on delete cascade
		, amount decimal(15, 2) not null
		, transaction_date date not null
		, transaction_type varchar(50) not null check (transaction_type in ('deposit', 'withdrawal'))
	);

insert into clients (name, age, registration_date) values
	('Иван Иванов', 30, '2019-05-15')
	, ('Мария Петрова', 25, '2020-01-10')
	, ('Алексей Сидоров', 40, '2021-03-22')
	, ('Елена Кузнецова', 35, '2020-07-19')
	, ('Дмитрий Смирнов', 28, '2022-11-05')
	, ('Ольга Васнецова', 50, '2018-12-30')
	, ('Сергей Козлов', 33, '2020-06-14')
	, ('Анна Морозова', 29, '2021-09-01')
	, ('Павел Новиков', 45, '2019-08-25')
	, ('Татьяна Павлова', 31, '2020-04-17');

insert into accounts (client_id, balance, open_date) values
	(1, 15000.00, '2019-05-20')
	, (1, 5000.00, '2020-02-10')
	, (2, 20000.00, '2020-01-15')
	, (3, 30000.00, '2021-03-25')
	, (4, 10000.00, '2020-07-25')
	, (5, 25000.00, '2022-11-10')
	, (6, 40000.00, '2019-01-05')
	, (7, 12000.00, '2020-06-20')
	, (8, 18000.00, '2021-09-05')
	, (9, 22000.00, '2019-09-01')
	, (10, 15000.00, '2020-04-20');

insert into transactions (account_id, amount, transaction_date, transaction_type) values
	(1, 1000.00, '2023-01-05', 'deposit')
	, (1, 500.00, '2023-01-10', 'withdrawal')
	, (2, 2000.00, '2023-02-15', 'deposit')
	, (2, 1000.00, '2023-02-20', 'withdrawal')
	, (3, 3000.00, '2023-03-25', 'deposit')
	, (3, 1500.00, '2023-03-30', 'withdrawal')
	, (4, 4000.00, '2023-04-05', 'deposit')
	, (4, 2000.00, '2023-04-10', 'withdrawal')
	, (5, 5000.00, '2023-05-15', 'deposit')
	, (5, 2500.00, '2023-05-20', 'withdrawal')
	, (6, 6000.00, '2023-06-25', 'deposit')
	, (6, 3000.00, '2023-06-30', 'withdrawal')
	, (7, 7000.00, '2023-07-05', 'deposit')
	, (7, 3500.00, '2023-07-10', 'withdrawal')
	, (8, 8000.00, '2023-08-15', 'deposit')
	, (8, 4000.00, '2023-08-20', 'withdrawal')
	, (9, 9000.00, '2023-09-25', 'deposit')
	, (9, 4500.00, '2023-09-30', 'withdrawal')
	, (10, 10000.00, '2023-10-05', 'deposit')
	, (10, 5000.00, '2023-10-10', 'withdrawal');


-- Используем CTE (Common Table Expression) для однократного сбора всей статистики по клиентам
WITH client_stats AS (
    -- Одним запросом получаем все необходимые агрегированные данные
    SELECT 
        a.client_id,
        -- Подсчитываем количество счетов клиента
        COUNT(DISTINCT a.account_id) AS total_accounts,
        -- Суммируем балансы по всем счетам
        SUM(a.balance) AS total_balance,
        -- Используем условный подсчет для транзакций:
        -- COUNT считает только те строки, где условие CASE возвращает NOT NULL
        COUNT(CASE WHEN t.transaction_type = 'deposit' THEN 1 END) AS total_deposits,
        COUNT(CASE WHEN t.transaction_type = 'withdrawal' THEN 1 END) AS total_withdrawals
    FROM accounts a
    -- LEFT JOIN сохраняет все счета, даже если по ним нет транзакций
    LEFT JOIN transactions t ON a.account_id = t.account_id
    -- Группируем по клиенту для получения агрегатов
    GROUP BY a.client_id
)
-- Основной запрос к таблице клиентов
SELECT 
    c.client_id, 
    c.name, 
    c.age,
    -- COALESCE заменяет NULL на 0 для клиентов без счетов
    COALESCE(cs.total_accounts, 0) AS total_accounts,
    COALESCE(cs.total_balance, 0) AS total_balance,
    COALESCE(cs.total_deposits, 0) AS total_deposits,
    COALESCE(cs.total_withdrawals, 0) AS total_withdrawals
FROM clients c
-- LEFT JOIN гарантирует, что клиенты без счетов также попадут в результат
LEFT JOIN client_stats cs ON c.client_id = cs.client_id
-- Фильтр по дате регистрации из условия задачи
WHERE c.registration_date >= '2020-01-01'
-- Сортировка по убыванию баланса согласно условию
-- NULLS LAST помещает клиентов без баланса в конец списка
ORDER BY cs.total_balance DESC NULLS LAST;

-- Что изменилось:
-- 1. Вместо 5 подзапросов (которые выполнялись для каждого клиента) один проход по данным
-- 2. Таблица accounts сканируется 1 раз вместо 3
-- 3. Таблица transactions сканируется 1 раз вместо 2
-- 4. Условная агрегация заменяет два отдельных подзапроса для разных типов транзакций
-- 5. Запрос масштабируется линейно с ростом данных, а не экспоненциально, т.к. изначально сложность была O(5*N*M), а стала O(N+M), где N - число клиентов, M - число счетов/транзакций


-- Результат --
-- |Мария Петрова|25|0|0|0|0
-- |Алексей Сидоров|40|0|0|0|0
-- |Елена Кузнецова|35|0|0|0|0
-- |Дмитрий Смирнов|28|0|0|0|0
-- |Сергей Козлов|33|0|0|0|0
-- |Анна Морозова|29|0|0|0|0
-- |Татьяна Павлова|31|0|0|0|0