CREATE INDEX land_registry_postcode_building_1_idx ON land_registry USING btree (postcode, building_1);
CREATE INDEX land_registry_transaction_date_1_idx ON land_registry USING btree (transaction_date);
