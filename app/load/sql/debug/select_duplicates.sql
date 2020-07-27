-- Product duplicates

select *
from product
where source_id in (select source_id
                    from product
                    group by source_id
                    having count(source_id) > 1)
group by source_id, id
order by source_id;

-- Review duplicates

select *
from review
where source_id in (select source_id
                    from review
                    group by source_id
                    having count(source_id) > 1)
group by source_id, id
order by source_id;


