-- name: drop-product-duplicates
delete
from product a
    using product b
where a.id > b.id
  and a.source_id = b.source_id;

-- name: drop-review-duplicates
delete
from review a
    using review b
where a.id > b.id
  and a.source_id = b.source_id;

-- name: drop-category-duplicates
delete
from category
where source_id = 410
  and name = 'computers';

delete
from category
where source_id = 7
  and name = 'computers';


delete
from category
where source_id = 588
  and name = 'computers';

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