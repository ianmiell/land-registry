--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: land_registry; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE land_registry (
    id character varying,
    created timestamp without time zone DEFAULT clock_timestamp(),
    price integer,
    transaction_date date,
    postcode character varying,
    type character(1),
    new_build character(1),
    estate_type character(1),
    building_1 character varying,
    building_2 character varying,
    street character varying,
    town character varying,
    city character varying,
    district character varying,
    county character varying,
    extra1 character(1),
    extra2 character(1)
);


ALTER TABLE public.land_registry OWNER TO postgres;

--
-- Name: postcode; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE postcode (
    postcode character varying,
    name character varying,
    x numeric,
    y numeric
);


ALTER TABLE public.postcode OWNER TO postgres;

--
-- Name: land_registry_postcode_building_1_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX land_registry_postcode_building_1_idx ON land_registry USING btree (postcode, building_1);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

