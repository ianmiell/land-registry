# Example crontab file; change folders accordingly
30 0 * * * cd /space/git/land_registry/bin && PATH=${PATH}:/space/git/shutit ./phoenix.sh > /tmp/lr_phoenix.log 2>&1
0 0 * * * docker run --volumes-from land_registry_db -v /media/storage_1/permanent_to_backup/land_registry_backups:/backup ubuntu tar cvf /backup/land_registry_db_backup.$(date +%Y%m%d).tar /var/bin/postgresql
0 0 * * * docker run --volumes-from land_registry_db -v /media/storage_1/permanent_to_backup/land_registry_backups:/backup ubuntu tar cvf /backup/land_registry_etc_backup.$(date +%Y%m%d).tar /etc/postgresql
