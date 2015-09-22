if [ `whoami` != "postgres" ]
then
	echo "Need to be postgres to run this"
	exit
fi
createuser -s land_registry
echo "alter user land_registry with password 'bitbucketandspoon'" | psql postgres
# give superuser for simpler perms
echo "alter user land_registry with superuser"

createuser reader
echo "alter user land_registry with password 'reader'" | psql postgres
echo "grant connect on database land_registry to reader" | psql postgres
echo "grant usage on schema public to reader" | psql postgres

