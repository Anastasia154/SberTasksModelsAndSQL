create table tranches
	(
		inn text
		, credit_num text
		, account text
		, operation_datetime timestamp
		, operation_sum numeric
		, doc_id numeric
	);

create table transactions
	(
		inn int8
		, account text
		, operation_datetime timestamp
		, operation_sum numeric
		, ctrg_inn int8
		, ctrg_account text
		, doc_id text
	);

insert into tranches (inn, credit_num, account, operation_datetime, operation_sum, doc_id) values
	('1234567890', 'CREDIT001', '40817810000000000001', '2024-01-01 10:00:00', 1000.00, 1)
	, ('1234567890', 'CREDIT002', '40817810000000000002', '2024-01-05 12:00:00', 1500.00, 2)
	, ('1234567890', 'CREDIT003', '40817810000000000003', '2024-01-10 14:00:00', 2000.00, 3)
	, ('2345678901', 'CREDIT004', '40817810000000000004', '2024-02-15 09:30:00', 3000.00, 4)
	, ('3456789012', 'CREDIT005', '40817810000000000005', '2024-03-20 16:45:00', 5000.00, 5)
	, ('4567890123', 'CREDIT006', '40817810000000000006', '2024-04-25 11:15:00', 7500.00, 6)
	, ('5678901234', 'CREDIT007', '40817810000000000007', '2024-05-30 14:20:00', 10000.00, 7)
	, ('6789012345', 'CREDIT008', '40817810000000000008', '2024-06-10 13:00:00', 12500.00, 8)
	, ('7890123456', 'CREDIT009', '40817810000000000009', '2024-07-15 10:45:00', 15000.00, 9)
	, ('8901234567', 'CREDIT010', '40817810000000000010', '2024-08-20 15:30:00', 20000.00, 10); 

insert into transactions (inn, account, operation_datetime, operation_sum, ctrg_inn, ctrg_account, doc_id) values
	(1234567890, '40817810000000000001', '2024-01-02 10:10:00', 900.00, 9876543210, '40817810000000000014', 'T1')
	, (2345678901, '40817810000000000004', '2024-02-17 11:20:00', 3500.00, 8765432109, '40817810000000000015', 'T2')
	, (1234567890, '40817810000000000003', '2024-01-15 14:05:00', 2500.00, 9876543210, '40817810000000000006', 'T3')
	, (2345678901, '40817810000000000004', '2024-02-16 10:10:00', 3200.00, 8765432109, '40817810000000000007', 'T4')
	, (7890123456, '40817810000000000009', '2024-07-18 10:15:00', 16000.00, 3210987654, '40817810000000000012', 'T5')
	, (1234567890, '40817810000000000002', '2024-01-06 12:05:00', 1500.00, 9876543210, '40817810000000000005', 'T6')
	, (5678901234, '40817810000000000007', '2024-06-01 14:40:00', 11000.00, 5432109876, '40817810000000000010', 'T7')
	, (6789012345, '40817810000000000008', '2024-06-12 13:50:00', 13000.00, 4321098765, '40817810000000000011', 'T8')
	, (3456789012, '40817810000000000005', '2024-03-22 15:20:00', 5500.00, 7654321098, '40817810000000000008', 'T9')
	, (8901234567, '40817810000000000010', '2024-08-22 15:25:00', 15000.00, 2109876543, '40817810000000000013', 'T10')
	, (1234567890, '40817810000000000001', '2024-01-01 10:05:00', 1000.00, 9876543210, '40817810000000000004', 'T11')
	, (4567890123, '40817810000000000006', '2024-04-27 11:30:00', 8000.00, 6543210987, '40817810000000000009', 'T12')
	, (8901234567, '40817810000000000010', '2024-08-25 16:30:00', 5800.00, 7654321098, '40817810000000000016', 'T13');



WITH 
-- Отбираем данные за 2024 год
filtered_tranches AS (
    SELECT 
        inn, 
        credit_num,
        account,
        operation_datetime,
        operation_sum,
        doc_id
    FROM tranches
    WHERE operation_datetime >= '2024-01-01' 
      AND operation_datetime < '2025-01-01'
),
filtered_transactions AS (
    SELECT 
        inn,
        account,
        operation_datetime,
        operation_sum,
        ctrg_inn,
        ctrg_account,
        doc_id
    FROM transactions
    WHERE operation_datetime >= '2024-01-01' 
      AND operation_datetime < '2025-01-01'
),

-- поиск операций с точным совпадением суммы в течение 10 дней после транша
exact_matches AS (
    SELECT 
        t.inn,
        t.credit_num,
        t.account as tranche_account,
        t.operation_datetime as tranche_datetime,
        t.operation_sum as tranche_sum,
        t.doc_id as tranche_doc_id,
        tr.ctrg_inn,
        tr.ctrg_account,
        tr.operation_datetime as transaction_datetime,
        tr.operation_sum as transaction_sum,
        tr.doc_id as transaction_doc_id,
        'exact_match' as match_type,  -- помечаем тип совпадения
        -- Рассчитываем разницу в днях (T+10)
        (tr.operation_datetime - t.operation_datetime) as days_diff,
        -- Вычисляем сумму транзакции, которая пошла в зачет транша (в данном случае вся сумма)
        tr.operation_sum as allocated_sum
    FROM filtered_tranches t
    INNER JOIN filtered_transactions tr 
        ON t.inn = tr.inn  -- Связываем по ИНН клиента
        AND t.account = tr.account  -- и по расчетному счету
        AND t.operation_sum = tr.operation_sum  -- Условие равенства сумм (копейка в копейку)
        AND tr.operation_datetime > t.operation_datetime  -- Транзакция после транша
        AND tr.operation_datetime <= date('t.operation_datetime', '10 days')
),

-- сбор всех расходных операций, превышающих сумму транша
-- Сначала для каждого транша находим все превышающие операции
potential_exceeds AS (
    SELECT 
        t.inn,
        t.credit_num,
        t.account as tranche_account,
        t.operation_datetime as tranche_datetime,
        t.operation_sum as tranche_sum,
        t.doc_id as tranche_doc_id,
        tr.ctrg_inn,
        tr.ctrg_account,
        tr.operation_datetime as transaction_datetime,
        tr.operation_sum as transaction_sum,
        tr.doc_id as transaction_doc_id,
        -- Рассчитываем разницу во времени
        (tr.operation_datetime - t.operation_datetime) as days_diff,
        -- Рассчитываем, какая часть суммы транзакции превышает сумму транша
        -- (если транзакция больше транша)
        tr.operation_sum - t.operation_sum as excess_amount,
        -- Сумма транша, которая покрывается этой транзакцией (полная сумма транша)
        t.operation_sum as allocated_sum
    FROM filtered_tranches t
    INNER JOIN filtered_transactions tr 
        ON t.inn = tr.inn
        AND t.account = tr.account
        AND tr.operation_sum > t.operation_sum  -- Только превышающие транзакции
        AND tr.operation_datetime > t.operation_datetime  -- После транша
),

-- Объединяем результаты и нумеруем
combined_results AS (
    SELECT 
        inn,
        credit_num,
        tranche_account,
        tranche_datetime,
        tranche_sum,
        tranche_doc_id,
        ctrg_inn,
        ctrg_account,
        transaction_datetime,
        transaction_sum,
        transaction_doc_id,
        match_type,
        days_diff,
        allocated_sum,
        -- Для превышающих транзакций дополнительная информация
        CASE WHEN match_type = 'exact_match' THEN NULL 
             ELSE transaction_sum - tranche_sum 
        END as excess_amount,
        -- Создаем уникальный идентификатор для группировки (транш + транзакция)
        ROW_NUMBER() OVER (PARTITION BY tranche_doc_id ORDER BY transaction_datetime) as rn
    FROM exact_matches
    
    UNION ALL
    
    SELECT 
        inn,
        credit_num,
        tranche_account,
        tranche_datetime,
        tranche_sum,
        tranche_doc_id,
        ctrg_inn,
        ctrg_account,
        transaction_datetime,
        transaction_sum,
        transaction_doc_id,
        'exceeds_match' as match_type,
        days_diff,
        allocated_sum,
        excess_amount,
        ROW_NUMBER() OVER (PARTITION BY tranche_doc_id ORDER BY transaction_datetime) as rn
    FROM potential_exceeds
    -- Исключаем транши, которые уже нашли точное совпадение
    WHERE tranche_doc_id NOT IN (SELECT DISTINCT tranche_doc_id FROM exact_matches)
)

SELECT 
    inn,
    credit_num,
    tranche_account,
    tranche_datetime,
    tranche_sum,
    tranche_doc_id,
    ctrg_inn,
    ctrg_account,
    transaction_datetime,
    transaction_sum,
    transaction_doc_id,
    match_type,
    CASE 
        WHEN match_type = 'exact_match' THEN 'Сумма совпадает полностью'
        ELSE CONCAT('Сумма транзакции превышает сумму транша на ', excess_amount)
    END as match_description,
    days_diff,
    allocated_sum
FROM combined_results
ORDER BY 
    inn, 
    tranche_datetime, 
    transaction_datetime;
	
	
-- Результат --
-- 1234567890|CREDIT003|40817810000000000003|2024-01-10 14:00:00|2000|3|9876543210|40817810000000000006|2024-01-15 14:05:00|2500|T3|exceeds_match|Сумма транзакции превышает сумму транша на 500|0|2000
-- 2345678901|CREDIT004|40817810000000000004|2024-02-15 09:30:00|3000|4|8765432109|40817810000000000007|2024-02-16 10:10:00|3200|T4|exceeds_match|Сумма транзакции превышает сумму транша на 200|0|3000
-- 2345678901|CREDIT004|40817810000000000004|2024-02-15 09:30:00|3000|4|8765432109|40817810000000000015|2024-02-17 11:20:00|3500|T2|exceeds_match|Сумма транзакции превышает сумму транша на 500|0|3000
-- 3456789012|CREDIT005|40817810000000000005|2024-03-20 16:45:00|5000|5|7654321098|40817810000000000008|2024-03-22 15:20:00|5500|T9|exceeds_match|Сумма транзакции превышает сумму транша на 500|0|5000
-- 4567890123|CREDIT006|40817810000000000006|2024-04-25 11:15:00|7500|6|6543210987|40817810000000000009|2024-04-27 11:30:00|8000|T12|exceeds_match|Сумма транзакции превышает сумму транша на 500|0|7500
-- 5678901234|CREDIT007|40817810000000000007|2024-05-30 14:20:00|10000|7|5432109876|40817810000000000010|2024-06-01 14:40:00|11000|T7|exceeds_match|Сумма транзакции превышает сумму транша на 1000|0|10000
-- 6789012345|CREDIT008|40817810000000000008|2024-06-10 13:00:00|12500|8|4321098765|40817810000000000011|2024-06-12 13:50:00|13000|T8|exceeds_match|Сумма транзакции превышает сумму транша на 500|0|12500
-- 7890123456|CREDIT009|40817810000000000009|2024-07-15 10:45:00|15000|9|3210987654|40817810000000000012|2024-07-18 10:15:00|16000|T5|exceeds_match|Сумма транзакции превышает сумму транша на 1000|0|15000