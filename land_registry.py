"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class land_registry(ShutItModule):


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
		shutit.install('telnet sudo adduser expect python-pygresql git python-pip wget')
		shutit.send('pip install shutit')
		shutit.send('groupadd -g 1000 land_registry')
		shutit.send('useradd -g land_registry -d /home/land_registry -s /bin/bash -m land_registry')
		shutit.send('adduser land_registry sudo')
		shutit.send('echo "%sudo ALL=(ALL:ALL) ALL" > /etc/sudoers.d/sudo')
		shutit.send('chmod 0440 /etc/sudoers.d/sudo')
		shutit.login('postgres')
		shutit.insert_text('fsync = off','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.insert_text('synchronous_commit = off','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.insert_text('maintenance_work_mem = 1024MB','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.insert_text('checkpoint_segments = 100','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.insert_text('host all  all    0.0.0.0/0  md5','/etc/postgresql/9.3/main/pg_hba.conf')
		shutit.insert_text("""listen_addresses='*'""",'/etc/postgresql/9.3/main/postgresql.conf',"#listen_addresses = 'localhost'")
		shutit.logout()
		shutit.send('/root/stop_postgres.sh')
		shutit.send('/root/start_postgres.sh')
		shutit.login('land_registry')
		shutit.send('''git clone --recursive https://github.com/ianmiell/land-registry.git''')
		shutit.send('''find . -name build.cnf | xargs chmod 0600''')
		shutit.logout()
		shutit.login('postgres')
		shutit.send('echo "create database land_registry" | psql')
		shutit.send('/home/land_registry/land_registry/context/bin/create_postgres_user.sh')
		shutit.send('cat /home/land_registry/land_registry/context/sql/SCHEMA.sql | psql land_registry')
		shutit.send('cat /home/land_registry/land_registry/context/sql/DROP_INDEX.sql | psql land_registry',timeout=99999)
		#shutit.send('cat /home/land_registry/land_registry/context/sql/DATA.sql | psql land_registry')
		shutit.send('''echo "copy postcode from '/home/land_registry/land_registry/context/postcodes/postcode.dat' delimiter ','" | psql land_registry''')   
		shutit.send('''echo 'create index land_registry_postcode_building_1_idx on land_registry (postcode, building_1)' | psql land_registry''')
		shutit.send('/home/land_registry/land_registry/context/bin/post_build.sh')
		shutit.logout()
		shutit.login('land_registry')
		shutit.send('cd /home/land_registry/land_registry/context/replenish/bin')
		shutit.send('./build.sh')
		#shutit.send('cd /home/land_registry/land_registry/context/backup_db/bin')
		#shutit.send('./build.sh')
		shutit.logout()
		shutit.login('postgres')
		shutit.send('cat /home/land_registry/land_registry/context/sql/CREATE_INDEX.sql | psql land_registry',timeout=99999)
		shutit.logout()
		shutit.delete_text('^fsync = off','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.delete_text('^synchronous_commit = off','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.delete_text('^maintenance_work_mem = 1024MB','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.delete_text('^checkpoint_segments = 100','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.send('/root/stop_postgres.sh')
		shutit.send('/root/start_postgres.sh')
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
	return land_registry(
		'tk.shutit.land_registry.land_registry', 1845506479.00,
		description='',
		maintainer='',
		delivery_methods=['docker'],
		depends=['shutit.tk.postgres.postgres']
	)

