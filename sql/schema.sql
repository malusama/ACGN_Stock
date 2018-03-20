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

--
-- TABLE: posts
--

CREATE TABLE posts (
    id                SERIAL PRIMARY KEY,
    body              TEXT                          NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    user_id           VARCHAR(255)                  NOT NULL
);


--
-- TABLE: stock
--
CREATE TABLE stock (
    id                SERIAL PRIMARY KEY,
    name              VARCHAR(255)                  NOT NULL UNIQUE,
    Introduction      TEXT                          DEFAULT NULL,
    cover             VARCHAR(255)                  DEFAULT NULL,
    image             VARCHAR(255)                  DEFAULT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
    user_id           VARCHAR(255)                  DEFAULT NULL
);


--
-- TABLE: bank
--
CREATE TABLE bank (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER                       NOT NULL,
    stock_id          INTEGER                       NOT NULL,
    stock_number      INTEGER                       NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);


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
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);


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
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);