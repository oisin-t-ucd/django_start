BEGIN;
--
-- Create model Category
--
CREATE TABLE "products_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL);
--
-- Add field categories to product
--
CREATE TABLE "products_product_categories" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "product_id" bigint NOT NULL REFERENCES "products_product" ("id") DEFERRABLE INITIALLY DEFERRED, "category_id" bigint NOT NULL REFERENCES "products_category" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "products_product_categories_product_id_category_id_a1f87bda_uniq" ON "products_product_categories" ("product_id", "category_id");
CREATE INDEX "products_product_categories_product_id_50ef8156" ON "products_product_categories" ("product_id");
CREATE INDEX "products_product_categories_category_id_27982bed" ON "products_product_categories" ("category_id");
COMMIT;