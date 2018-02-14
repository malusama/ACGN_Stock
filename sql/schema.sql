--
-- TABLE: users
--

CREATE TABLE users (
    id                SERIAL PRIMARY KEY,
    nickname          VARCHAR(255)                  NOT NULL,
    password          VARCHAR(255)                  NOT NULL,
    email             VARCHAR(255)                  DEFAULT NULL UNIQUE,
   	currency          INTEGER                       DEFAULT NULL,
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
	Total             INTEGER                       DEFAULT NULL NOT NULL,
	Price             INTEGER                       DEFAULT NULL NOT NULL,
	Introduction      TEXT                          DEFAULT NULL,
	cover             VARCHAR(255)                  DEFAULT NULL,
	image             VARCHAR(255)                  DEFAULT NULL,
	created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);


--
-- TABLE: bank
--
CREATE TABLE bank (
	id                SERIAL PRIMARY KEY,
	user_id           VARCHAR(255)                  NOT NULL,
	stock_id          VARCHAR(255)                  NOT NULL,
	stock_number      VARCHAR(255)                  NOT NULL,
	created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);