"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class land_registry(ShutItModule):


	def build(self, shutit):
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
		shutit.send('/home/land_registry/land-registry/context/bin/create_postgres_user.sh')
		shutit.send('cat /home/land_registry/land-registry/context/sql/SCHEMA.sql | psql land_registry')
		shutit.send('cat /home/land_registry/land-registry/context/sql/DROP_INDEX.sql | psql land_registry',timeout=99999)
		shutit.send('''echo "copy postcode from '/home/land_registry/land-registry/context/postcodes/postcode.dat' delimiter ','" | psql land_registry''')   
		shutit.send('''echo 'create index land_registry_postcode_building_1_idx on land_registry (postcode, building_1)' | psql land_registry''')
		shutit.send('/home/land_registry/land-registry/context/bin/post_build.sh')
		shutit.logout()
		shutit.login('land_registry')
		shutit.send('cd /home/land_registry/land-registry/context/replenish/bin')
		shutit.send('./build.sh')
		shutit.logout()
		shutit.login('postgres')
		shutit.send('cat /home/land_registry/land-registry/context/sql/CREATE_INDEX.sql | psql land_registry',timeout=99999)
		shutit.logout()
		shutit.delete_text('^fsync = off','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.delete_text('^synchronous_commit = off','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.delete_text('^maintenance_work_mem = 1024MB','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.delete_text('^checkpoint_segments = 100','/etc/postgresql/9.3/main/postgresql.conf')
		shutit.send('/root/stop_postgres.sh')
		shutit.send('/root/start_postgres.sh')
		return True

	def get_config(self, shutit):
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

