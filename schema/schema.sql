SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = ON;
SET check_function_bodies = FALSE;
SET client_min_messages = WARNING;
SET search_path = PUBLIC, extensions;
SET default_tablespace = '';
SET default_with_oids = FALSE;

-- this extension allow to generate uuid as default field, gen_random_uuid - function from this extension
-- https://stackoverflow.com/questions/11584749/how-to-create-a-new-database-with-the-hstore-extension-already-installed

-- CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS public.order_status CASCADE;
DROP TABLE IF EXISTS public.order CASCADE;
DROP TABLE IF EXISTS public.payment_type CASCADE;
DROP TABLE IF EXISTS public.payment_status CASCADE;
DROP TABLE IF EXISTS public.order_payment CASCADE;
DROP TABLE IF EXISTS public.service CASCADE;
DROP TABLE IF EXISTS public.service_type CASCADE;
DROP TABLE IF EXISTS public.user_service CASCADE;
DROP TABLE IF EXISTS public.user_service_status CASCADE;

CREATE TABLE public.service_type
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(100) NOT NULL
);

CREATE TABLE public.payment_type
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(100)
);

CREATE TABLE public.order_status
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(100)
);

CREATE TABLE public.payment_status
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(100)
);

CREATE TABLE public.user_service_status
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(100)
);

CREATE TABLE public.service
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(100) NOT NULL
  , description VARCHAR(500)
  , type_id INT REFERENCES public.service_type(id) NOT NULL
  , price NUMERIC NOT NULL
  , old_price NUMERIC
  , billed_period INT
  , is_free BOOLEAN DEFAULT FALSE
  , is_trial BOOLEAN DEFAULT FALSE
  , trial_period_days INT DEFAULT NULL
  , modify_date TIMESTAMP NOT NULL DEFAULT now()
  , modify_reason TEXT NOT NULL DEFAULT 'init'
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.order
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , code SERIAL UNIQUE
  , status_id INT REFERENCES public.order_status(id) NOT NULL
  , modify_date TIMESTAMP NOT NULL DEFAULT now()
  , modify_reason TEXT NOT NULL DEFAULT 'init'
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.order_payment
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , order_uuid UUID REFERENCES public.order(uuid) NOT NULL
  , type_id INT REFERENCES public.payment_type(id) NOT NULL
  , status_id INT REFERENCES public.payment_status(id) NOT NULL
  , json_data JSON NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.user_service
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , user_uuid UUID NOT NULL
  , service_id INT REFERENCES public.service(id) NOT NULL
  , order_uuid UUID REFERENCES public.order(uuid) NOT NULL
  , status_id INT REFERENCES public.user_service_status(id) NOT NULL
  , is_trial BOOLEAN DEFAULT FALSE
  , expire_date TIMESTAMP
  , modify_date TIMESTAMP NOT NULL DEFAULT now()
  , modify_reason TEXT NOT NULL DEFAULT 'init'
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);