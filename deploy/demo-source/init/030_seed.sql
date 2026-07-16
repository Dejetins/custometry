\set ON_ERROR_STOP on
\include /tmp/custometry-profile.psql

INSERT INTO retail.channels (channel_id, channel_code, channel_name)
VALUES
    (1, 'retail', 'Retail stores'),
    (2, 'online', 'Online store'),
    (3, 'marketplace', 'Marketplace'),
    (4, 'wholesale', 'Wholesale');

INSERT INTO retail.stores (store_id, store_code, store_name, region, opened_on)
SELECT
    store_id,
    'ST-' || lpad(store_id::text, 3, '0'),
    'Northwind Store ' || store_id,
    (ARRAY['North', 'South', 'East', 'West'])[(store_id - 1) % 4 + 1],
    DATE '2018-01-01' + ((store_id * 41) % 1000)
FROM generate_series(1, :store_count) AS store_id;

INSERT INTO retail.customers (
    customer_id,
    first_name,
    last_name,
    email,
    loyalty_card,
    city,
    created_at,
    valid_from,
    valid_to
)
SELECT
    customer_id,
    'Customer' || customer_id,
    'Demo' || ((customer_id * 17) % 101),
    CASE WHEN customer_id % 11 = 0 THEN NULL ELSE 'customer' || customer_id || '@example.test' END,
    CASE WHEN customer_id % 7 = 0 THEN NULL ELSE 'LC-' || lpad(customer_id::text, 8, '0') END,
    (ARRAY['Helsinki', 'Riga', 'Tallinn', 'Vilnius', 'Stockholm'])[(customer_id - 1) % 5 + 1],
    timestamptz '2020-01-01 00:00:00+00' + ((customer_id * 19) % 1400) * interval '1 day',
    timestamptz '2020-01-01 00:00:00+00',
    CASE WHEN customer_id % 97 = 0 THEN timestamptz '2025-01-01 00:00:00+00' ELSE NULL END
FROM generate_series(1, :customer_count) AS customer_id;

INSERT INTO retail.external_customer_records (source_namespace, source_customer_id, display_name)
SELECT namespace, source_customer_id, namespace || ' Customer ' || source_customer_id
FROM unnest(ARRAY['northwind-retail', 'legacy-retail']) AS namespace
CROSS JOIN generate_series(1, LEAST(25, :customer_count)) AS source_customer_id;

INSERT INTO retail.customer_history (
    customer_version_id,
    customer_id,
    city,
    valid_from,
    valid_to
)
SELECT
    customer_id * 10 + version_number,
    customer_id,
    'History City ' || version_number,
    CASE
        WHEN version_number = 1 THEN timestamptz '2023-01-01 00:00:00+00'
        WHEN customer_id % 2 = 0 THEN timestamptz '2023-06-26 00:00:00+00'
        ELSE timestamptz '2023-07-06 00:00:00+00'
    END,
    CASE
        WHEN version_number = 1 THEN timestamptz '2023-07-01 00:00:00+00'
        ELSE timestamptz '2024-01-01 00:00:00+00'
    END
FROM generate_series(1, LEAST(20, :customer_count)) AS customer_id
CROSS JOIN generate_series(1, 2) AS version_number;

INSERT INTO retail.calendar (calendar_date, iso_year, iso_week, month_start, is_period_complete)
SELECT
    calendar_date,
    EXTRACT(isoyear FROM calendar_date)::integer,
    EXTRACT(week FROM calendar_date)::integer,
    date_trunc('month', calendar_date)::date,
    calendar_date < DATE '2025-12-01'
FROM generate_series(DATE '2020-12-28', DATE '2025-12-31', interval '1 day') AS calendar_date;

INSERT INTO retail.products (
    product_id,
    sku,
    product_name,
    brand,
    category,
    subcategory,
    currency,
    list_price,
    valid_from,
    valid_to
)
SELECT
    product_id,
    'SKU-' || lpad(product_id::text, 5, '0'),
    'Demo Product ' || product_id,
    'Brand ' || ((product_id - 1) % 12 + 1),
    (ARRAY['Food', 'Home', 'Beauty', 'Electronics', 'Apparel'])[(product_id - 1) % 5 + 1],
    'Subcategory ' || ((product_id - 1) % 20 + 1),
    'EUR',
    round((4.50 + ((product_id * 37) % 19500) / 100.0)::numeric, 2),
    timestamptz '2020-01-01 00:00:00+00',
    CASE WHEN product_id % 53 = 0 THEN timestamptz '2025-06-30 00:00:00+00' ELSE NULL END
FROM generate_series(1, :product_count) AS product_id;

INSERT INTO retail.promotions (
    promotion_id,
    promotion_name,
    starts_at,
    ends_at,
    audience_type,
    status,
    discount_percent
)
SELECT
    promotion_id,
    'Campaign ' || promotion_id,
    timestamptz '2024-01-01 00:00:00+00' + (promotion_id * 20) * interval '1 day',
    timestamptz '2024-01-01 00:00:00+00' + (promotion_id * 20 + 21 + promotion_id % 8) * interval '1 day',
    (ARRAY['all_customers', 'segment_snapshot', 'customer_list'])[(promotion_id - 1) % 3 + 1],
    (ARRAY['actual', 'actual', 'planned'])[(promotion_id - 1) % 3 + 1],
    5 + (promotion_id % 6) * 2.5
FROM generate_series(1, :promotion_count) AS promotion_id;

INSERT INTO retail.promotion_channels (promotion_id, channel_id)
SELECT promotion_id, (promotion_id - 1) % 4 + 1
FROM generate_series(1, :promotion_count) AS promotion_id
UNION ALL
SELECT promotion_id, promotion_id % 4 + 1
FROM generate_series(4, :promotion_count, 4) AS promotion_id;

INSERT INTO retail.promotion_customers (promotion_id, customer_id, audience_version)
SELECT
    promotion_id,
    ((promotion_id * 83 + member_number * 17) % :customer_count) + 1,
    'audience-v1'
FROM generate_series(1, :promotion_count) AS promotion_id
CROSS JOIN generate_series(1, :audience_member_count) AS member_number
WHERE (promotion_id - 1) % 3 <> 0;

INSERT INTO retail.receipts (
    receipt_id,
    receipt_number,
    receipt_datetime,
    customer_id,
    store_id,
    channel_id,
    currency,
    gross_amount,
    discount_amount,
    net_amount,
    status,
    updated_at
)
SELECT
    receipt_id,
    'R-' || lpad(receipt_id::text, 9, '0'),
    timestamptz '2024-01-01 08:00:00+00'
        + ((receipt_id - 1) % 731) * interval '1 day'
        + ((receipt_id * 13) % 720) * interval '1 minute',
    CASE WHEN receipt_id % 19 = 0 THEN NULL ELSE (receipt_id * 31) % :customer_count + 1 END,
    (receipt_id * 7) % :store_count + 1,
    (receipt_id * 11) % 4 + 1,
    CASE WHEN receipt_id % 211 = 0 THEN 'SEK' ELSE 'EUR' END,
    round((20 + (receipt_id * 29) % 38000 / 100.0)::numeric, 2),
    round(((receipt_id * 7) % 3000 / 100.0)::numeric, 2),
    CASE
        WHEN receipt_id % 29 = 0 THEN -round((10 + (receipt_id * 17) % 9000 / 100.0)::numeric, 2)
        ELSE round((20 + (receipt_id * 29) % 38000 / 100.0 - (receipt_id * 7) % 3000 / 100.0)::numeric, 2)
    END,
    CASE
        WHEN receipt_id % 29 = 0 THEN 'returned'
        WHEN receipt_id % 113 = 0 THEN 'cancelled'
        ELSE 'completed'
    END,
    timestamptz '2024-01-01 08:00:00+00'
        + ((receipt_id - 1) % 731) * interval '1 day'
        + ((receipt_id * 13) % 720) * interval '1 minute'
        + (receipt_id % 17) * interval '1 hour'
FROM generate_series(1, :receipt_count) AS receipt_id;

INSERT INTO retail.receipt_items (
    receipt_item_id,
    receipt_id,
    product_id,
    quantity,
    unit_price,
    discount_amount,
    net_amount
)
SELECT
    receipt_id * 10 + line_number,
    receipt_id,
    CASE
        WHEN receipt_id % 997 = 0 AND line_number = 3 THEN 999999
        ELSE (receipt_id * 7 + line_number * 13) % :product_count + 1
    END,
    CASE WHEN receipt_id % 29 = 0 THEN -1 ELSE (receipt_id + line_number) % 4 + 1 END,
    round((4.50 + ((receipt_id * 23 + line_number * 17) % 19500) / 100.0)::numeric, 2),
    round((((receipt_id + line_number) * 5) % 750 / 100.0)::numeric, 2),
    round((
        (CASE WHEN receipt_id % 29 = 0 THEN -1 ELSE (receipt_id + line_number) % 4 + 1 END)
        * (4.50 + ((receipt_id * 23 + line_number * 17) % 19500) / 100.0)
        - (((receipt_id + line_number) * 5) % 750 / 100.0)
    )::numeric, 2)
FROM generate_series(1, :receipt_count) AS receipt_id
CROSS JOIN generate_series(1, :items_per_receipt) AS line_number;

INSERT INTO retail.returns (
    return_id,
    original_receipt_id,
    return_datetime,
    reason_code,
    status
)
SELECT
    receipt_id / 29,
    receipt_id,
    receipt_datetime + interval '3 days',
    (ARRAY['damaged', 'wrong_item', 'changed_mind'])[((receipt_id / 29) - 1) % 3 + 1],
    'accepted'
FROM retail.receipts
WHERE receipt_id % 29 = 0;

INSERT INTO retail.return_items (
    return_item_id,
    return_id,
    original_receipt_item_id,
    quantity,
    net_amount
)
SELECT
    receipt_id / 29,
    receipt_id / 29,
    receipt_id * 10 + 1,
    1,
    -abs(net_amount)
FROM retail.receipts
WHERE receipt_id % 29 = 0;

ANALYZE retail.channels;
ANALYZE retail.stores;
ANALYZE retail.customers;
ANALYZE retail.external_customer_records;
ANALYZE retail.customer_history;
ANALYZE retail.calendar;
ANALYZE retail.products;
ANALYZE retail.promotions;
ANALYZE retail.promotion_channels;
ANALYZE retail.promotion_customers;
ANALYZE retail.receipts;
ANALYZE retail.receipt_items;
ANALYZE retail.returns;
ANALYZE retail.return_items;
