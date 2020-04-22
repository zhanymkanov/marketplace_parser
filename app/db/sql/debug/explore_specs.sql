-- Product specs without type, but with GPU
select *
from specs
where type is null
  and gpu is not null;

-- Product specs without type, but with CPU
select *
from specs
where type is null
  and cpu is not null;

-- Product without type, but with CPU
select *
from product
where product.source_id in (select product_id
                            from specs
                            where type is null
                              and cpu is not null);

-- Type counts of all
select type, count(*)
from specs
group by type
order by count(*) desc;

-- Type counts of important PC types
select type, count(*)
from specs
where type in ('ноутбук', 'системный блок', 'игровой ноутбук', 'моноблок',
               'ультрабук')
group by type;

-- Select products without GPU info, but game laptops
select *
from product
where source_id in (select product_id
                    from specs
                    where type = 'игровой ноутбук'
                      and gpu is null);

-- Used for validation of absenting the types like book
select distinct type
from specs
where type like '%бук';

-- Used for validation of absenting the types like block
select distinct type
from specs
where type like '%блок';

-- Count of All GPU usages
select type, gpu, count(*)
from specs
where gpu is not null
group by type, gpu
order by count(*) desc, gpu;

-- Count of laptops GPU usages
select type, gpu, count(*)
from specs
where type like '%бук%'
  and gpu is not null
group by type, gpu
order by count(*) desc, gpu;

-- Count of PC GPU usages
select type, gpu, count(*)
from specs
where type like '%блок'
group by type, gpu
order by count(*) desc, gpu;

-- CPUs only of laptops and PCs
select type, cpu, count(*)
from specs
where cpu is not null and (type  like '%блок ' or type like '%бук')
group by cpu, type
order by count(*) desc ;