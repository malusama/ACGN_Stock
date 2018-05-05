--
-- TABLE: stock_tag
--
CREATE TABLE stock_tag (
    id                SERIAL PRIMARY KEY,
    tag               VARCHAR(255)                  NOT NULL UNIQUE,
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);
