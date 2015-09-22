-- transaction count ordered by month
select count(*), extract(year from transaction_date), extract(month from transaction_date)
from land_registry
where postcode like 'SW8%'
group by 2, 3 order by 2,3;

-- date truncation
select count(*), date_trunc('month', transaction_date)
from land_registry
where city = 'LONDON'
group by 2
order by 2;

-- csv to stdout
copy (select * from land_registry limit 1)
to stdout
with csv header;  

-- postcodes near a single point (WC1)
select postcode || '%'
from postcodes
where latitude < 51.525 + 0.1
and latitude > 51.525 - 0.1
and longitude > -0.116 - 0.1
and longitude < -0.116 + 0.1; 

-- postcodes by month, distance from WC1.
select count(*), date_trunc('month',transaction_date)
from land_registry
where substring(postcode,'([A-Z0-9]*) .*') in (
	select postcode 
	from postcodes 
	where latitude < 51.525 + 0.1
	and latitude > 51.525 - 0.1
	and longitude > -0.116 - 0.1
	and longitude < -0.116 + 0.1
)
group by 2
order by 2
desc;

