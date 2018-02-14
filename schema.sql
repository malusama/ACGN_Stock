--
-- TABLE: zro_image
--

CREATE TABLE zro_image (
    id                SERIAL PRIMARY KEY,
    place_name        VARCHAR(255)                  NOT NULL,
    acg_id            INTEGER                       DEFAULT NULL,
    acg_name          VARCHAR(255)                  DEFAULT NULL,
    image             TEXT                          DEFAULT '',
    source			  VARCHAR(255)                  DEFAULT NULL,
    part			  VARCHAR(255)                  DEFAULT NULL,
    introduction	  TEXT                          DEFAULT '',
    updated_at        TIMESTAMP                     DEFAULT now() NOT NULL,
    created_at        TIMESTAMP                     DEFAULT now() NOT NULL
);

CREATE INDEX zro_image_acg_id
    ON zro_image (acg_id)
