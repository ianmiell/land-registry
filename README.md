Land Registry
-------------

Land registry database tracker.


```
git clone --recursive https://github.com/ianmiell/land-registry.git
cd land-registry/bin
./phoenix.sh
```

Example crons for backing up the database and running nightly are in bin/cron.sh



PLAN:

```
land_registry_db - volume mounts the datbase itself
land_registry_updater - cronjob caller
land_registry_pggraph - grapher

land_registry_db:
  image: postgres:9.5
  volumes:
    - /var/dockervolumes...:/var/lib/postgresql
  expose:
    - "5432"
  container_name: land_registry_db

land_registry_updater:

```
