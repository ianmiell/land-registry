#!/bin/bash
echo "grant select on land_registry to reader" | psql land_registry
