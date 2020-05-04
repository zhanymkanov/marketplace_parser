-- name: create-category
create table if not exists category
(
    id         serial primary key,
    source_id  bigint,
    name       text,
    created_at date default current_date
);

-- name: create-product
create table if not exists product
(
    id               serial primary key,
    source_id        bigint,
    category_id      int,
    title            text,
    price_unit       int,
    price_sale       int,
    url              text,
    brand            text,
    rating           smallint,
    reviews_quantity int,
    created_at       date default current_date
);


-- name: create-specs
create table if not exists specs
(
    id         serial primary key,
    product_id bigint,
    type       text,
    cpu        text,
    hertz      smallint,
    cores      smallint,
    gpu        text,
    ram        smallint,
    ram_type   text,
    ssd        bool,
    drive_size smallint,
    extra      jsonb,
    created_at date default current_date
);

-- name: create-review
create table if not exists review
(
    id              serial primary key,
    source_id       bigint,
    product_id      bigint,
    date            date,
    rating          float,
    comment_plus    text,
    comment_minus   text,
    comment_text    text,
    review_approved smallint,
    review_rated    smallint,
    created_at      date default current_date
);

-- name: create-gpu-rating
create table if not exists gpu_rating
(
    id     serial primary key,
    gpu    text,
    rate   float4,
    versus text
);

-- name: create-cpu-rating
create table if not exists cpu_rating
(
    id     serial primary key,
    cpu    text,
    rate   float4,
    versus text
);

-- name: create-view-desktops
create materialized view desktops as
select p.id        p_id,
       c.name      category_name,
       p.source_id p_source_id,
       title,
       price_sale  price,
       brand,
       rating,
       reviews_quantity,
       s.cpu,
       cr.rate     cpu_rate,
       hertz,
       cores,
       s.gpu,
       gr.rate     gpu_rate,
       ram,
       ram_type,
       ssd,
       drive_size,
       url
from product p
         join category c on p.category_id = c.source_id
         join specs s on p.source_id = s.product_id
         join cpu_rating cr on s.cpu = cr.cpu
         join gpu_rating gr on s.gpu = gr.gpu
where name = 'desktops';

-- name: create-view-notebooks
create materialized view notebooks as
select p.id        p_id,
       c.name      category_name,
       p.source_id p_source_id,
       title,
       price_sale  price,
       brand,
       rating,
       reviews_quantity,
       s.cpu,
       cr.rate     cpu_rate,
       hertz,
       cores,
       s.gpu,
       gr.rate     gpu_rate,
       ram,
       ram_type,
       ssd,
       drive_size,
       url
from product p
         join category c on p.category_id = c.source_id
         join specs s on p.source_id = s.product_id
         join cpu_rating cr on s.cpu = cr.cpu
         join gpu_rating gr on s.gpu = gr.gpu
where name = 'notebooks';
