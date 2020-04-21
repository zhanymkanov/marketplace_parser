-- name: drop-category-indexes
alter table category
    drop constraint category_source_id;

-- name: drop-product-indexes
BEGIN;

alter table product
    drop constraint product_source_id;

alter table product
    drop constraint product_url;

alter table product
    drop constraint product_category_fk_source_id;

alter table product
    drop constraint product_specs_fk_id;

COMMIT;


-- name: drop-specs-indexes
BEGIN;

alter table specs
    drop constraint specs_product_id;

alter table specs
    drop constraint specs_product_fk_source_id;

COMMIT;

-- name: drop-review-indexes
BEGIN;

alter table review
    drop constraint review_source_id;

alter table review
    drop constraint review_product_fk_source_id;

COMMIT;


-- name: drop-cpu-rating-indexes
BEGIN;

alter table cpu_rating
    drop constraint cpu_rating_unique;

COMMIT;

-- name: drop-gpu-rating-indexes
BEGIN;

alter table gpu_rating
    drop constraint gpu_rating_unique;

COMMIT;
