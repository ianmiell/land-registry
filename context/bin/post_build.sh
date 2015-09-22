#!/bin/bash
echo "grant select on land_registry to reader" | psql postgres
