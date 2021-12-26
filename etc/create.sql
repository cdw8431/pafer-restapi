
CREATE TABLE "user" (
    "id" SERIAL PRIMARY KEY,
    "email" VARCHAR(64) NOT NULL UNIQUE,
    "password" VARCHAR(256)   NOT NULL,
    "created" TIMESTAMP   NOT NULL
);

CREATE TABLE "card" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT   NOT NULL,
    "category_id" INT   NOT NULL,
    "card" VARCHAR(64)   NOT NULL,
    "image_url" TEXT   NOT NULL,
    "is_favorite" BOOLEAN   NOT NULL,
    "created" TIMESTAMP   NOT NULL
);

CREATE TABLE "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT   NOT NULL,
    "category" VARCHAR(64)   NOT NULL,
    "description" VARCHAR(255)   NOT NULL,
    "created" TIMESTAMP   NOT NULL
);

CREATE TABLE "field" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT   NOT NULL,
    "field" VARCHAR(64)   NOT NULL,
    "type" VARCHAR(32)   NOT NULL,
    "created" TIMESTAMP   NOT NULL
);

CREATE TABLE "card_fileds" (
    "id" SERIAL PRIMARY KEY,
    "card_id" INT   NOT NULL,
    "filed_id" INT   NOT NULL,
    "content" TEXT   NOT NULL,
    "order" INT   NOT NULL
);

ALTER TABLE "card" ADD CONSTRAINT "fk_card_user_id" FOREIGN KEY("user_id")
REFERENCES "user" ("id");

ALTER TABLE "card" ADD CONSTRAINT "fk_card_category_id" FOREIGN KEY("category_id")
REFERENCES "category" ("id");

ALTER TABLE "category" ADD CONSTRAINT "fk_category_user_id" FOREIGN KEY("user_id")
REFERENCES "user" ("id");

ALTER TABLE "field" ADD CONSTRAINT "fk_field_user_id" FOREIGN KEY("user_id")
REFERENCES "user" ("id");

ALTER TABLE "card_fileds" ADD CONSTRAINT "fk_card_fileds_card_id" FOREIGN KEY("card_id")
REFERENCES "card" ("id");

ALTER TABLE "card_fileds" ADD CONSTRAINT "fk_card_fileds_filed_id" FOREIGN KEY("filed_id")
REFERENCES "field" ("id");

