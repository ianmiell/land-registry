"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule
import time

class replenish(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches)
		#                                    - Returns True if any lines in output match any of
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		#
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		# If there's over a million rows in land_registry, assume we don't need to do the full whack.
		shutit.send(r'''wget -qO- http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/price-paid-data/pp-complete.csv | sed 's/\r//g' > /tmp/all.csv''')
		shutit.send(''' echo "copy (select id, price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra from land_registry) to '/tmp/lr.csv' with (format csv, delimiter ',', force_quote *)" | psql land_registry''');
		shutit.send('''sort /tmp/all.csv | sed 's/ 00:00//' > /tmp/all.csv.sorted''')
		shutit.send('sort /tmp/lr.csv > /tmp/lr.csv.sorted')
		shutit.send('comm -1 -3 /tmp/lr.csv.sorted /tmp/all.csv.sorted > /tmp/add.csv')
		shutit.send('comm -2 -3 /tmp/lr.csv.sorted /tmp/all.csv.sorted > /tmp/delete.csv')
		shutit.send('wc -l /tmp/delete.csv')
		shutit.send('wc -l /tmp/add.csv')
		# insert
		shutit.send(r'''cat <(cat <(echo ID,PRICE,DATE,POSTCODE,TYPE,NEW_BUILD,ESTATE_TYPE,BUILDING_NO,BUILDING_NAME,STREET,TOWN,CITY,DISTRICT,COUNTY,EXTRA) <(cat /tmp/add.csv)) > /tmp/insert.csv''')
		shutit.send('''echo 'create table land_registry_tmp (id varchar, price integer, transaction_date date, postcode varchar, type char(1), new_build char(1), estate_type char(1), building_1 varchar, building_2 varchar, street varchar, town varchar, city varchar, district varchar, county varchar, extra char(1));' | psql land_registry''')
		shutit.send('''echo "copy land_registry_tmp from '/tmp/insert.csv' delimiter ',' csv header;" | psql land_registry''')
		shutit.send('''echo "insert into land_registry (id, price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra) select id, price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra from land_registry_tmp" | psql land_registry''',timeout=999999)
		shutit.send('''echo "drop table land_registry_tmp" | psql land_registry''')
		# delete
		shutit.send('''echo 'create table land_registry_tmp (id varchar, price integer, transaction_date date, postcode varchar, type char(1), new_build char(1), estate_type char(1), building_1 varchar, building_2 varchar, street varchar, town varchar, city varchar, district varchar, county varchar, extra char(1));' | psql land_registry''')
		shutit.send('''echo "copy land_registry_tmp from '/tmp/delete.csv' delimiter ',' csv header" | psql land_registry''')
		shutit.send('''echo "delete from land_registry where id in (select id from land_registry_tmp)" | psql land_registry''')
		shutit.send('''echo "drop table land_registry_tmp" | psql land_registry''')
		shutit.send('rm -f /tmp/*.csv',check_exit=False)
		for year in (time.localtime()[0],time.localtime()[0]-1):
			shutit.send('rm -f /tmp/all.csv',check_exit=False)
			shutit.send(r'''cat <(cat <(echo ID,PRICE,DATE,POSTCODE,TYPE,NEW_BUILD,ESTATE_TYPE,BUILDING_NO,BUILDING_NAME,STREET,TOWN,CITY,DISTRICT,COUNTY,EXTRA) <(wget -qO- http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/price-paid-data/pp-''' + str(year) + r'''.csv | sed 's/\r//g')) > /tmp/all.csv''')
			shutit.send('''echo 'create table land_registry_tmp (id varchar, price integer, transaction_date date, postcode varchar, type char(1), new_build char(1), estate_type char(1), building_1 varchar, building_2 varchar, street varchar, town varchar, city varchar, district varchar, county varchar, extra char(1));' | psql land_registry''')
			shutit.send('''echo "copy land_registry_tmp from '/tmp/all.csv' delimiter ',' csv header;" | psql land_registry''')
			#delete from land_registry rows that don't exist in the download
			shutit.send("""echo "delete from land_registry l1 where not exists (select 1 from land_registry_tmp l2 where l2.price = l1.price and l2.transaction_date = l1.transaction_date and l2.postcode = l1.postcode and l2.type = l1.type and l2.new_build = l1.new_build and l2.estate_type = l1.estate_type and l2.building_1 = l1.building_1 and l2.building_2 = l1.building_2 and l2.street = l1.street and l2.town = l1.town and l2.city = l1.city and l2.district = l1.district and l2.county = l1.county and l2.extra = l1.extra) and transaction_date >= '""" + str(year) + """-01-01' and transaction_date < '""" + str(year+1) + """-01-01'" | psql land_registry""",timeout=999999)
			#insert into land registry rows that exist in land_registry_tmp but not in land_registry
			shutit.send('''echo "insert into land_registry (price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra) select price, transaction_date, postcode, type, new_build, estate_type, building_1, building_2, street, town, city, district, county, extra from land_registry_tmp l1 where not exists (select 1 from land_registry l2 where l2.price = l1.price and l2.transaction_date = l1.transaction_date and l2.postcode = l1.postcode and l2.type = l1.type and l2.new_build = l1.new_build and l2.estate_type = l1.estate_type and l2.building_1 = l1.building_1 and l2.building_2 = l1.building_2 and l2.street = l1.street and l2.town = l1.town and l2.city = l1.city and l2.district = l1.district and l2.county = l1.county and l2.extra = l1.extra)" | psql land_registry''',timeout=999999)
			shutit.send('''echo "drop table land_registry_tmp" | psql land_registry''')
			shutit.send('rm -f /tmp/all.csv',check_exit=False)
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

