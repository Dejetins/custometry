\set ON_ERROR_STOP on

SELECT jsonb_build_object(
    'schema_version', '1.0.0',
    'counts', jsonb_build_object(
        'channels', (SELECT count(*) FROM retail.channels),
        'stores', (SELECT count(*) FROM retail.stores),
        'customers', (SELECT count(*) FROM retail.customers),
        'external_customer_records', (SELECT count(*) FROM retail.external_customer_records),
        'customer_history', (SELECT count(*) FROM retail.customer_history),
        'calendar', (SELECT count(*) FROM retail.calendar),
        'products', (SELECT count(*) FROM retail.products),
        'promotions', (SELECT count(*) FROM retail.promotions),
        'promotion_channels', (SELECT count(*) FROM retail.promotion_channels),
        'promotion_customers', (SELECT count(*) FROM retail.promotion_customers),
        'receipts', (SELECT count(*) FROM retail.receipts),
        'receipt_items', (SELECT count(*) FROM retail.receipt_items),
        'returns', (SELECT count(*) FROM retail.returns),
        'return_items', (SELECT count(*) FROM retail.return_items)
    ),
    'scenarios', jsonb_build_object(
        'anonymous_receipts', (SELECT count(*) FROM retail.receipts WHERE customer_id IS NULL),
        'returns', (SELECT count(*) FROM retail.returns),
        'cancellations', (SELECT count(*) FROM retail.receipts WHERE status = 'cancelled'),
        'multi_currency', (SELECT count(DISTINCT currency) FROM retail.receipts),
        'late_updates', (SELECT count(*) FROM retail.receipts WHERE updated_at > receipt_datetime),
        'missing_product_reference', (
            SELECT count(*)
            FROM retail.receipt_items AS item
            LEFT JOIN retail.products AS product USING (product_id)
            WHERE item.product_id IS NOT NULL AND product.product_id IS NULL
        ),
        'scd_end_dates', (
            (SELECT count(*) FROM retail.customers WHERE valid_to IS NOT NULL)
            + (SELECT count(*) FROM retail.products WHERE valid_to IS NOT NULL)
        ),
        'leap_day', (SELECT count(*) FROM retail.calendar WHERE calendar_date = DATE '2024-02-29'),
        'overlapping_promotion_windows', (
            SELECT count(*)
            FROM retail.promotions AS left_promotion
            JOIN retail.promotions AS right_promotion
              ON left_promotion.promotion_id < right_promotion.promotion_id
             AND tstzrange(left_promotion.starts_at, left_promotion.ends_at, '[)')
                 && tstzrange(right_promotion.starts_at, right_promotion.ends_at, '[)')
        ),
        'multi_channel_promotions', (
            SELECT count(*)
            FROM (
                SELECT promotion_id
                FROM retail.promotion_channels
                GROUP BY promotion_id
                HAVING count(*) > 1
            ) AS multi_channel
        ),
        'segment_and_customer_list_audiences', (
            SELECT count(DISTINCT audience_type)
            FROM retail.promotions
            WHERE audience_type IN ('segment_snapshot', 'customer_list')
              AND EXISTS (
                  SELECT 1
                  FROM retail.promotion_customers
                  WHERE promotion_customers.promotion_id = promotions.promotion_id
              )
        ),
        'duplicate_source_ids_across_namespaces', (
            SELECT count(*)
            FROM (
                SELECT source_customer_id
                FROM retail.external_customer_records
                GROUP BY source_customer_id
                HAVING count(DISTINCT source_namespace) > 1
            ) AS duplicated
        ),
        'overlapping_and_gapped_scd_intervals', (
            SELECT count(*)
            FROM retail.customer_history AS first_version
            JOIN retail.customer_history AS second_version
              ON first_version.customer_id = second_version.customer_id
             AND first_version.customer_version_id < second_version.customer_version_id
            WHERE first_version.valid_to <> second_version.valid_from
        ),
        'iso_week_53', (SELECT count(*) FROM retail.calendar WHERE iso_week = 53),
        'incomplete_current_month', (SELECT count(*) FROM retail.calendar WHERE NOT is_period_complete)
    ),
    'kpis', jsonb_build_object(
        'completed_receipts', (SELECT count(*) FROM retail.receipts WHERE status = 'completed'),
        'returned_receipts', (SELECT count(*) FROM retail.receipts WHERE status = 'returned'),
        'cancelled_receipts', (SELECT count(*) FROM retail.receipts WHERE status = 'cancelled'),
        'receipt_date_min', (SELECT min(receipt_datetime)::date::text FROM retail.receipts),
        'receipt_date_max', (SELECT max(receipt_datetime)::date::text FROM retail.receipts),
        'receipt_net_amount', (SELECT to_char(sum(net_amount), 'FM999999999999990.00') FROM retail.receipts),
        'item_net_amount', (SELECT to_char(sum(net_amount), 'FM999999999999990.00') FROM retail.receipt_items)
    )
)::text;
