
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL PRIMARY KEY,
    "email" VARCHAR(64) NOT NULL UNIQUE,
    "nickname" VARCHAR(64) NOT NULL UNIQUE,
    "password" VARCHAR(256) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "card" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "category_id" INT NOT NULL,
    "card" VARCHAR(64) NOT NULL,
    "image_url" TEXT NOT NULL,
    "is_favorite" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "category" VARCHAR(64) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "field" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "field" VARCHAR(64) NOT NULL,
    "type" VARCHAR(32) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "card_fileds" (
    "id" SERIAL PRIMARY KEY,
    "card_id" INT NOT NULL,
    "filed_id" INT NOT NULL,
    "content" TEXT NOT NULL,
    "order" INT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
