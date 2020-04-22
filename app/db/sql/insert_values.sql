-- name: bulk-insert-categories
begin;
insert into category(name, source_id)
VALUES (:name, :source_id);
commit;

-- name: bulk-insert-products
begin;
insert into product(source_id, category_id, title,
                    price_unit, price_sale, url,
                    brand, rating, reviews_quantity)
values (:source_id, :category_id, :title,
        :price_unit, :price_sale, :url,
        :brand, :rating, :reviews_quantity);
commit;

-- name: bulk-insert-product-details
begin;
insert into product_details(product_id, details)
values (:product_id, :details);
commit;

-- name: bulk-insert-reviews
begin;
insert into review(source_id, product_id, date,
                   rating, comment_plus, comment_minus,
                   comment_text, review_approved, review_rated)
values (:source_id, :product_id, :date,
        :rating, :comment_plus, :comment_minus,
        :comment_text, :review_approved, :review_rated);
commit;

-- name: bulk-insert-specs
begin;
insert into specs(product_id, type, cpu, hertz, cores, gpu, ram, ram_type,
                  ssd, drive_size, extra)
values (:product_id, :type, :cpu, :hertz, :cores, :gpu, :ram, :ram_type,
        :ssd, :drive_size, :extra);
commit;
