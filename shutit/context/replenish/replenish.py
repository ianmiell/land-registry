"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule
import time

class replenish(ShutItModule):


	def build(self, shutit):
		# Get the download from LR and sort it
		shutit.send('rm -f /tmp/*.csv',check_exit=False)
		shutit.send(r'''wget -qO- http://publicdata.landregistry.gov.uk/market-trend-data/price-paid-data/a/pp-complete.csv | sed 's/\r//g' > /tmp/all.csv''',timeout=99999)
		shutit.send('''sort /tmp/all.csv | sed 's/ 00:00//' > /tmp/all.csv.sorted''')
		# Drop indexes for speedier inserts and updates
		shutit.send('echo "drop index land_registry_postcode_building_1_idx" | psql -U postgres -h landregistrydb land_registry')
		shutit.send('echo "drop index land_registry_transaction_date_1_idx" | psql -U postgres -h landregistrydb land_registry')
		# Extract current state of table and sort it
		shutit.send('''echo "copy (select id, price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra1, extra2 from land_registry) to STDOUT with (format csv, delimiter ',', force_quote *)" | psql -U postgres -h landregistrydb land_registry > /tmp/lr.csv''')
		shutit.send('sort /tmp/lr.csv | uniq > /tmp/lr.csv.sorted')
		# add csv
		shutit.send('comm -1 -3 /tmp/lr.csv.sorted /tmp/all.csv.sorted > /tmp/add.csv')
		shutit.send('echo ROWS TO ADD && wc -l /tmp/add.csv')
		# Set up land_registry_tmp table
		shutit.send('''echo "drop table land_registry_tmp" | psql -U postgres -h landregistrydb land_registry''')
		shutit.send('''echo 'create table land_registry_tmp (id varchar, price integer, transaction_date date, postcode varchar, type char(1), new_build char(1), estate_type char(1), building_1 varchar, building_2 varchar, street varchar, town varchar, city varchar, district varchar, county varchar, extra1 char(1), extra2 char(1));' | psql -U postgres -h landregistrydb land_registry''')
		# insert file
		shutit.send('''echo "copy land_registry_tmp from STDIN delimiter ',' csv header;" > /tmp/insert.csv''') # SQL header for inserting csv
		shutit.send(r'''cat <(cat <(echo ID,PRICE,DATE,POSTCODE,TYPE,NEW_BUILD,ESTATE_TYPE,BUILDING_NO,BUILDING_NAME,STREET,TOWN,CITY,DISTRICT,COUNTY,EXTRA1,EXTRA2) <(cat /tmp/add.csv)) >> /tmp/insert.csv''')
		shutit.send('''psql -U postgres -h landregistrydb land_registry < /tmp/insert.csv''')
		shutit.send('''echo "insert into land_registry (id, price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra1, extra2) select id, price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra1, extra2 from land_registry_tmp" | psql -U postgres -h landregistrydb land_registry''',timeout=999999)
		# Items to delete
		shutit.send('''echo "copy land_registry_tmp from STDIN delimiter ',' csv header;" > /tmp/delete.csv''')
		shutit.send('comm -2 -3 /tmp/lr.csv.sorted /tmp/all.csv.sorted >> /tmp/delete.csv')
		shutit.send('echo ROWS TO DELETE && wc -l /tmp/delete.csv')
		# Set up land_registry_tmp table
		shutit.send('''echo "drop table land_registry_tmp" | psql -U postgres -h landregistrydb land_registry''')
		shutit.send('''echo 'create table land_registry_tmp (id varchar, price integer, transaction_date date, postcode varchar, type char(1), new_build char(1), estate_type char(1), building_1 varchar, building_2 varchar, street varchar, town varchar, city varchar, district varchar, county varchar, extra1 char(1), extra2 char(1));' | psql -U postgres -h landregistrydb land_registry''')
		# delete
		shutit.send('''psql -U postgres -h landregistrydb land_registry < /tmp/delete.csv''')
		shutit.send('''echo "delete from land_registry where id in (select id from land_registry_tmp)" | psql -U postgres -h landregistrydb land_registry''')
		# Drop the temporary table
		shutit.send('''echo "drop table land_registry_tmp" | psql -U postgres -h landregistrydb land_registry''')
		shutit.send('echo "create index land_registry_postcode_building_1_idx ON land_registry USING btree (postcode, building_1);" | psql -U postgres -h landregistrydb land_registry') 
		shutit.send('echo "create index land_registry_transaction_date_1_idx ON land_registry USING btree (transaction_date);" | psql -U postgres -h landregistrydb land_registry') 
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

