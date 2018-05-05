--
-- TABLE: stock_magnet
--
CREATE TABLE stock_magnet (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER                       NOT NULL,
    stock_id          INTEGER                       NOT NULL,
    Magnet            TEXT                          NOT NULL,
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);


--
-- TABLE: stock_tag
--
CREATE TABLE stock_tag (
    id                SERIAL PRIMARY KEY,
    tag               VARCHAR(255)                  NOT NULL UNIQUE,
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);


ALTER TABLE stock
	ADD works_series TEXT DEFAULT NULL;
ALTER TABLE stock
	ADD release_time VARCHAR(255) DEFAULT NULL;
ALTER TABLE stock
	ADD length_time VARCHAR(255) DEFAULT NULL;
ALTER TABLE stock
	ADD company VARCHAR(255) DEFAULT NULL;
ALTER TABLE stock
	ADD factory VARCHAR(255) DEFAULT NULL;
ALTER TABLE stock
	ADD category VARCHAR(255) DEFAULT NULL;
ALTER TABLE stock
	ADD Screenshots TEXT DEFAULT NULL;
