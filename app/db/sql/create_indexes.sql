-- name: create-category-indexes
alter table category
    add constraint category_source_id
        unique (source_id);

-- name: create-product-indexes
BEGIN;
alter table product
    add constraint product_source_id
        unique (source_id);

alter table product
    add constraint product_url
        unique (url);

alter table product
    add constraint product_category_fk_source_id
        foreign key (category_id)
            references category (source_id)
            on delete set null;

alter table product
    add constraint product_specs_fk_id
        foreign key (specs_id)
            references specs (id)
            on delete set null;
COMMIT;

-- name: create-specs-indexes
BEGIN;

alter table specs
    add constraint specs_product_id
        unique (product_id);

alter table specs
    add constraint specs_product_fk_source_id
        foreign key (product_id)
            references product (source_id)
            on delete cascade;

COMMIT;

-- name: create-review-indexes
BEGIN;

alter table review
    add constraint review_source_id
        unique (source_id);

alter table review
    add constraint review_product_fk_source_id
        foreign key (product_id)
            references product (source_id)
            on delete set null;

COMMIT;

-- name: create-cpu-rating-indexes
BEGIN;

alter table cpu_rating
    add constraint cpu_rating_unique
        unique (cpu);

COMMIT;

-- name: create-gpu-rating-indexes
BEGIN;

alter table gpu_rating
    add constraint gpu_rating_unique
        unique (gpu);

COMMIT;
