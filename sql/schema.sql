--
-- TABLE: users
--

CREATE TABLE users (
    id                SERIAL PRIMARY KEY,
    nickname          VARCHAR(255)                  NOT NULL,
    password          VARCHAR(255)                  NOT NULL,
    email             VARCHAR(255)                  DEFAULT NULL UNIQUE,
    currency          INTEGER                       DEFAULT NULL,
    Authority         INTEGER                       DEFAULT NULL,
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);
CREATE INDEX users_id
    ON users (id);
CREATE INDEX user_nickname
    ON users (nickname);


--
-- TABLE: posts
--

CREATE TABLE posts (
    id                SERIAL PRIMARY KEY,
    body              TEXT                          NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    user_id           INTEGER                  		NOT NULL
);
CREATE INDEX posts_users_id
    ON posts (user_id);

--
-- TABLE: stock
--
CREATE TABLE stock (
    id                SERIAL PRIMARY KEY,
    name              VARCHAR(255)                  NOT NULL UNIQUE,
    Introduction      TEXT                          DEFAULT NULL,
    cover             VARCHAR(255)                  DEFAULT NULL,
    image             VARCHAR(255)                  DEFAULT NULL,
    user_id           VARCHAR(255)                  DEFAULT NULL,
    works_series      TEXT                          DEFAULT NULL,
    release_time      TIMESTAMP                  	DEFAULT NULL,
    length_time       VARCHAR(255)                  DEFAULT NULL,
    company           VARCHAR(255)                  DEFAULT NULL,
    factory           VARCHAR(255)                  DEFAULT NULL,
    category          VARCHAR(255)                  DEFAULT NULL,
    Screenshots       TEXT                          DEFAULT NULL,
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);
CREATE INDEX stock_user_id
    ON stock (user_id);
CREATE INDEX stock_release_time
    ON stock (release_time);
CREATE INDEX stock_company
    ON stock (company);
CREATE INDEX stock_factory
    ON stock (factory);
--
-- TABLE: bank
--
CREATE TABLE bank (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER                       NOT NULL,
    stock_id          INTEGER                       NOT NULL,
    stock_number      INTEGER                       NOT NULL,
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);
CREATE INDEX bank_user_id
    ON bank (user_id);
CREATE INDEX bank_stock_id
    ON bank (stock_id);
--
-- TABLE: stock_order
--
CREATE TABLE stock_order (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER                       NOT NULL,
    stock_id          INTEGER                       NOT NULL,
    stock_number      INTEGER                       NOT NULL,
    stock_price       INTEGER                       NOT NULL,
    order_type        INTEGER                       NOT NULL,
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);
CREATE INDEX stock_order_user_id
    ON stock_order (user_id);
CREATE INDEX stock_order_stock_id
    ON stock_order (stock_id);
CREATE INDEX stock_order_order_type
    ON stock_order (order_type);
CREATE INDEX stock_order_stock_price
    ON stock_order (stock_price);


--
-- TABLE: stock_apply
--
CREATE TABLE stock_apply (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER                       NOT NULL,
    apply_status      INTEGER                       NOT NULL,
    stock_name        VARCHAR(255)                  NOT NULL UNIQUE,
    cover             VARCHAR(255)                  DEFAULT NULL,
    image             VARCHAR(255)                  DEFAULT NULL,
    Introduction      TEXT                          DEFAULT NULL,
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);
CREATE INDEX stock_apply_user_id
    ON stock_apply (user_id);
CREATE INDEX stock_apply_apply_status
    ON stock_apply (apply_status);
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
CREATE INDEX stock_magnet_stock_id
    ON stock_magnet (stock_id);
CREATE INDEX stock_magnet_user_id
    ON stock_magnet (user_id);