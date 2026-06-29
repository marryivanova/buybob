from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "categories" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "slug" VARCHAR(200) NOT NULL,
    "name" VARCHAR(200) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "config" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "label" VARCHAR(200) NOT NULL,
    "key" VARCHAR(20) NOT NULL UNIQUE,
    "value" JSONB NOT NULL,
    "status" SMALLINT NOT NULL DEFAULT 1
);
COMMENT ON COLUMN "config"."status" IS 'on: 1\noff: 0';
CREATE TABLE IF NOT EXISTS "departments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "employees" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "full_name" VARCHAR(255) NOT NULL,
    "password_hash" VARCHAR(255) NOT NULL,
    "department_id" INT REFERENCES "departments" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "suppliers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "inn" VARCHAR(12) NOT NULL,
    "contact_name" VARCHAR(100) NOT NULL,
    "email" VARCHAR(100) NOT NULL,
    "phone" VARCHAR(20) NOT NULL
);
CREATE TABLE IF NOT EXISTS "products" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "unit" VARCHAR(5) NOT NULL DEFAULT 'шт',
    "quantity" DECIMAL(10,2) NOT NULL,
    "price" DECIMAL(12,2) NOT NULL,
    "status" VARCHAR(9) NOT NULL DEFAULT 'в наличии',
    "expiry_date" DATE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "category_id" INT REFERENCES "categories" ("id") ON DELETE CASCADE,
    "supplier_id" INT NOT NULL REFERENCES "suppliers" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "products"."unit" IS 'KG: кг\nLITERS: литры\nPCS: шт\nGRAMS: гр';
COMMENT ON COLUMN "products"."status" IS 'IN_STOCK: в наличии\nORDERED: заказан\nSHIPPED: отгружен\nWRITTEN_OFF: списан';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = ()
