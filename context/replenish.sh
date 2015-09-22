#!/bin/bash

rm -f /tmp/all.csv
cat <(cat <(echo ID,PRICE,DATE,POSTCODE,TYPE,NEW_BUILD,ESTATE_TYPE,BUILDING_NO,BUILDING_NAME,STREET,TOWN,CITY,DISTRICT,COUNTY,EXTRA) <(wget -qO- http://publicdata.landregistry.gov.uk/market-trend-data/price-paid-data/a/pp-complete.csv | sed 's/\r//g')) > /tmp/all.csv


echo 'create table land_registry_tmp (id varchar, price integer, transaction_date date, postcode varchar, type char(1), new_build char(1), estate_type char(1), building_1 varchar, building_2 varchar, street varchar, town varchar, city varchar, district varchar, county varchar, extra char(1));' | psql land_registry
echo "copy land_registry_tmp from '/tmp/all.csv' delimiter ',' csv header;" | psql land_registry


#delete from land_registry rows that don't exist in the donwload
echo "delete from land_registry l1 where not exists (select 1 from land_registry_tmp l2 where l2.price = l1.price and l2.transaction_date = l1.transaction_date and l2.postcode = l1.postcode and l2.type = l1.type and l2.new_build = l1.new_build and l2.estate_type = l1.estate_type and l2.building_1 = l1.building_1 and l2.building_2 = l1.building_2 and l2.street = l1.street and l2.town = l1.town and l2.city = l1.city and l2.district = l1.district and l2.county = l1.county and l2.extra = l1.extra)" | psql land_registry

#insert into land registry rows that exist in land_registry_tmp but not in land_registry
echo "insert into land_registry (price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra) select price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra from land_registry_tmp l1 where not exists (select 1 from land_registry l2 where l2.price = l1.price and l2.transaction_date = l1.transaction_date and l2.postcode = l1.postcode and l2.type = l1.type and l2.new_build = l1.new_build and l2.estate_type = l1.estate_type and l2.building_1 = l1.building_1 and l2.building_2 = l1.building_2 and l2.street = l1.street and l2.town = l1.town and l2.city = l1.city and l2.district = l1.district and l2.county = l1.county and l2.extra = l1.extra)" | psql land_registry


echo "drop table land_registry_tmp" | psql land_registry

rm -f /tmp/all.csv
#TODO: detect changes / trigger 

