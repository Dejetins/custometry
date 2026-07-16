\set ON_ERROR_STOP on

CREATE SCHEMA retail;

CREATE TABLE retail.channels (
    channel_id integer PRIMARY KEY,
    channel_code text NOT NULL UNIQUE,
    channel_name text NOT NULL
);

CREATE TABLE retail.stores (
    store_id integer PRIMARY KEY,
    store_code text NOT NULL UNIQUE,
    store_name text NOT NULL,
    region text NOT NULL,
    opened_on date NOT NULL
);

CREATE TABLE retail.customers (
    customer_id bigint PRIMARY KEY,
    source_namespace text NOT NULL DEFAULT 'northwind-retail',
    first_name text NOT NULL,
    last_name text NOT NULL,
    email text,
    loyalty_card text,
    city text NOT NULL,
    created_at timestamptz NOT NULL,
    valid_from timestamptz NOT NULL,
    valid_to timestamptz
);

CREATE TABLE retail.external_customer_records (
    source_namespace text NOT NULL,
    source_customer_id bigint NOT NULL,
    display_name text NOT NULL,
    PRIMARY KEY (source_namespace, source_customer_id)
);

CREATE TABLE retail.customer_history (
    customer_version_id bigint PRIMARY KEY,
    customer_id bigint NOT NULL REFERENCES retail.customers(customer_id),
    city text NOT NULL,
    valid_from timestamptz NOT NULL,
    valid_to timestamptz NOT NULL,
    CHECK (valid_to > valid_from)
);

CREATE TABLE retail.calendar (
    calendar_date date PRIMARY KEY,
    iso_year integer NOT NULL,
    iso_week integer NOT NULL,
    month_start date NOT NULL,
    is_period_complete boolean NOT NULL
);

CREATE TABLE retail.products (
    product_id bigint PRIMARY KEY,
    sku text NOT NULL UNIQUE,
    product_name text NOT NULL,
    brand text NOT NULL,
    category text NOT NULL,
    subcategory text NOT NULL,
    currency char(3) NOT NULL,
    list_price numeric(12, 2) NOT NULL,
    valid_from timestamptz NOT NULL,
    valid_to timestamptz
);

CREATE TABLE retail.promotions (
    promotion_id bigint PRIMARY KEY,
    promotion_name text NOT NULL,
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    audience_type text NOT NULL,
    status text NOT NULL,
    discount_percent numeric(5, 2) NOT NULL,
    CHECK (ends_at > starts_at)
);

CREATE TABLE retail.promotion_channels (
    promotion_id bigint NOT NULL REFERENCES retail.promotions(promotion_id),
    channel_id integer NOT NULL REFERENCES retail.channels(channel_id),
    PRIMARY KEY (promotion_id, channel_id)
);

CREATE TABLE retail.promotion_customers (
    promotion_id bigint NOT NULL REFERENCES retail.promotions(promotion_id),
    customer_id bigint NOT NULL REFERENCES retail.customers(customer_id),
    audience_version text NOT NULL,
    PRIMARY KEY (promotion_id, customer_id)
);

CREATE TABLE retail.receipts (
    receipt_id bigint PRIMARY KEY,
    receipt_number text NOT NULL UNIQUE,
    receipt_datetime timestamptz NOT NULL,
    customer_id bigint,
    store_id integer NOT NULL REFERENCES retail.stores(store_id),
    channel_id integer NOT NULL REFERENCES retail.channels(channel_id),
    currency char(3) NOT NULL,
    gross_amount numeric(14, 2) NOT NULL,
    discount_amount numeric(14, 2) NOT NULL,
    net_amount numeric(14, 2) NOT NULL,
    status text NOT NULL,
    updated_at timestamptz NOT NULL
);

CREATE TABLE retail.receipt_items (
    receipt_item_id bigint PRIMARY KEY,
    receipt_id bigint NOT NULL REFERENCES retail.receipts(receipt_id),
    product_id bigint,
    quantity numeric(12, 3) NOT NULL,
    unit_price numeric(12, 2) NOT NULL,
    discount_amount numeric(12, 2) NOT NULL,
    net_amount numeric(14, 2) NOT NULL
);

CREATE TABLE retail.returns (
    return_id bigint PRIMARY KEY,
    original_receipt_id bigint NOT NULL REFERENCES retail.receipts(receipt_id),
    return_datetime timestamptz NOT NULL,
    reason_code text NOT NULL,
    status text NOT NULL
);

CREATE TABLE retail.return_items (
    return_item_id bigint PRIMARY KEY,
    return_id bigint NOT NULL REFERENCES retail.returns(return_id),
    original_receipt_item_id bigint NOT NULL REFERENCES retail.receipt_items(receipt_item_id),
    quantity numeric(12, 3) NOT NULL,
    net_amount numeric(14, 2) NOT NULL
);

CREATE INDEX receipts_customer_datetime_idx
    ON retail.receipts (customer_id, receipt_datetime);
CREATE INDEX receipt_items_receipt_idx
    ON retail.receipt_items (receipt_id);
CREATE INDEX returns_original_receipt_idx
    ON retail.returns (original_receipt_id);
CREATE INDEX customer_history_customer_validity_idx
    ON retail.customer_history (customer_id, valid_from, valid_to);
