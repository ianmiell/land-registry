"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule
import time

class replenish(ShutItModule):


	def build(self, shutit):
		shutit.send(r'''wget -qO- http://publicdata.landregistry.gov.uk/market-trend-data/price-paid-data/a/pp-complete.csv | sed 's/\r//g' > /tmp/all.csv''',timeout=99999)
		shutit.send(''' echo "copy (select id, price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra from land_registry) to '/tmp/lr.csv' with (format csv, delimiter ',', force_quote *)" | psql land_registry''');
		shutit.send('''sort /tmp/all.csv | sed 's/ 00:00//' > /tmp/all.csv.sorted''')
		shutit.send('sort /tmp/lr.csv > /tmp/lr.csv.sorted')
		shutit.send('comm -1 -3 /tmp/lr.csv.sorted /tmp/all.csv.sorted > /tmp/add.csv')
		shutit.send('comm -2 -3 /tmp/lr.csv.sorted /tmp/all.csv.sorted > /tmp/delete.csv')
		shutit.send('wc -l /tmp/delete.csv')
		shutit.send('wc -l /tmp/add.csv')
		# insert
		shutit.send(r'''cat <(cat <(echo ID,PRICE,DATE,POSTCODE,TYPE,NEW_BUILD,ESTATE_TYPE,BUILDING_NO,BUILDING_NAME,STREET,TOWN,CITY,DISTRICT,COUNTY,EXTRA1,EXTRA2) <(cat /tmp/add.csv)) > /tmp/insert.csv''')
		shutit.send('''echo 'create table land_registry_tmp (id varchar, price integer, transaction_date date, postcode varchar, type char(1), new_build char(1), estate_type char(1), building_1 varchar, building_2 varchar, street varchar, town varchar, city varchar, district varchar, county varchar, extra1 char(1), extra2 char(1));' | psql land_registry''')
		shutit.send('''echo "copy land_registry_tmp from '/tmp/insert.csv' delimiter ',' csv header;" | psql land_registry''')
		shutit.send('''echo "insert into land_registry (id, price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra) select id, price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra from land_registry_tmp" | psql land_registry''',timeout=999999)
		shutit.send('''echo "drop table land_registry_tmp" | psql land_registry''')
		# delete
		shutit.send('''echo 'create table land_registry_tmp (id varchar, price integer, transaction_date date, postcode varchar, type char(1), new_build char(1), estate_type char(1), building_1 varchar, building_2 varchar, street varchar, town varchar, city varchar, district varchar, county varchar, extra char(1));' | psql land_registry''')
		shutit.send('''echo "copy land_registry_tmp from '/tmp/delete.csv' delimiter ',' csv header" | psql land_registry''')
		shutit.send('''echo "delete from land_registry where id in (select id from land_registry_tmp)" | psql land_registry''')
		shutit.send('''echo "drop table land_registry_tmp" | psql land_registry''')
		shutit.send('rm -f /tmp/*.csv',check_exit=False)
		#for year in (time.localtime()[0],time.localtime()[0]-1):
		#	shutit.send('rm -f /tmp/all.csv',check_exit=False)
		#	shutit.send(r'''cat <(cat <(echo ID,PRICE,DATE,POSTCODE,TYPE,NEW_BUILD,ESTATE_TYPE,BUILDING_NO,BUILDING_NAME,STREET,TOWN,CITY,DISTRICT,COUNTY,EXTRA) <(wget -qO- http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/price-paid-data/pp-''' + str(year) + r'''.csv | sed 's/\r//g')) > /tmp/all.csv''')
		#	shutit.send('''echo 'create table land_registry_tmp (id varchar, price integer, transaction_date date, postcode varchar, type char(1), new_build char(1), estate_type char(1), building_1 varchar, building_2 varchar, street varchar, town varchar, city varchar, district varchar, county varchar, extra char(1));' | psql land_registry''')
		#	shutit.send('''echo "copy land_registry_tmp from '/tmp/all.csv' delimiter ',' csv header;" | psql land_registry''')
		#	#delete from land_registry rows that don't exist in the download
		#	shutit.send("""echo "delete from land_registry l1 where not exists (select 1 from land_registry_tmp l2 where l2.price = l1.price and l2.transaction_date = l1.transaction_date and l2.postcode = l1.postcode and l2.type = l1.type and l2.new_build = l1.new_build and l2.estate_type = l1.estate_type and l2.building_1 = l1.building_1 and l2.building_2 = l1.building_2 and l2.street = l1.street and l2.town = l1.town and l2.city = l1.city and l2.district = l1.district and l2.county = l1.county and l2.extra = l1.extra) and transaction_date >= '""" + str(year) + """-01-01' and transaction_date < '""" + str(year+1) + """-01-01'" | psql land_registry""",timeout=999999)
		#	#insert into land registry rows that exist in land_registry_tmp but not in land_registry
		#	shutit.send('''echo "insert into land_registry (price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra) select price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra from land_registry_tmp l1 where not exists (select 1 from land_registry l2 where l2.price = l1.price and l2.transaction_date = l1.transaction_date and l2.postcode = l1.postcode and l2.type = l1.type and l2.new_build = l1.new_build and l2.estate_type = l1.estate_type and l2.building_1 = l1.building_1 and l2.building_2 = l1.building_2 and l2.street = l1.street and l2.town = l1.town and l2.city = l1.city and l2.district = l1.district and l2.county = l1.county and l2.extra = l1.extra)" | psql land_registry''',timeout=999999)
		#	shutit.send('''echo "drop table land_registry_tmp" | psql land_registry''')
		#	shutit.send('rm -f /tmp/all.csv',check_exit=False)
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return replenish(
		'land_registry.replenish.replenish.replenish', 120223214.00,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup']
	)

