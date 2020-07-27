-- name: drop-product-duplicates
delete
from product a
    using product b
where a.id < b.id
  and a.source_id = b.source_id;

-- name: drop-review-duplicates
delete
from review a
    using review b
where a.id > b.id
  and a.source_id = b.source_id;

-- name: drop-category-duplicates
delete
from review
where product_id not in (select distinct source_id from product);

delete
from category a
    using category b
where a.id < b.id
  and a.source_id = b.source_id;


-- name: drop-cpu-rating-duplicates
delete
from cpu_rating a
    using cpu_rating b
where a.id > b.id
  and a.cpu = b.cpu;

-- name: drop-gpu-rating-duplicates
delete
from gpu_rating a
    using gpu_rating b
where a.id > b.id
  and a.gpu = b.gpu;