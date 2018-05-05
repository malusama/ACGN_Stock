--
-- TABLE: stock_order
--
CREATE TABLE stock_order (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER                       NOT NULL,
    stock_id          INTEGER                       NOT NULL,
    stock_number      INTEGER                       NOT NULL,
    type              INTEGER                       NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);
