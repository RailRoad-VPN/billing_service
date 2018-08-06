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

DROP TABLE IF EXISTS public.user_subscription CASCADE;
DROP TABLE IF EXISTS public.user_subscription_status CASCADE;
DROP TABLE IF EXISTS public.order_status CASCADE;
DROP TABLE IF EXISTS public.order CASCADE;
DROP TABLE IF EXISTS public.payment_type CASCADE;
DROP TABLE IF EXISTS public.payment_status CASCADE;
DROP TABLE IF EXISTS public.order_payment CASCADE;
DROP TABLE IF EXISTS public.subscription CASCADE;
DROP TABLE IF EXISTS public.subscription_translation CASCADE;
DROP TABLE IF EXISTS public.subscription_feature CASCADE;
DROP TABLE IF EXISTS public.subscription_feature_translation CASCADE;


CREATE TABLE public.subscription
(
    id SERIAL PRIMARY KEY
  , price_per_month NUMERIC NOT NULL
  , old_price_per_month NUMERIC
  , billed_period_in_months INT NOT NULL
  , billed_period_in_years INT NOT NULL
  , is_best BOOLEAN DEFAULT FALSE
  , modify_date TIMESTAMP NOT NULL DEFAULT now()
  , modify_reason TEXT NOT NULL DEFAULT 'init'
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.subscription_translation
(
    id SERIAL PRIMARY KEY
  , subscription_id INT REFERENCES public.subscription(id) NOT NULL
  , name VARCHAR(200) NOT NULL
  , description VARCHAR(200) NOT NULL
  , bill_freq VARCHAR(200)
  , price_freq VARCHAR(200)
  , lang_code CHAR(2)
);

CREATE TABLE public.subscription_feature
(
    id SERIAL PRIMARY KEY
  , subscription_id INT REFERENCES public.subscription(id) NOT NULL
  , enabled BOOLEAN NOT NULL DEFAULT FALSE
  , modify_date TIMESTAMP NOT NULL DEFAULT now()
  , modify_reason TEXT NOT NULL DEFAULT 'init'
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.subscription_feature_translation
(
    id SERIAL PRIMARY KEY
  , subscription_feature_id INT REFERENCES public.subscription_feature(id) NOT NULL
  , name VARCHAR(200) NOT NULL
  , tooltip VARCHAR(300)
  , lang_code CHAR(2)
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

CREATE TABLE public.user_subscription_status
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(100)
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

CREATE TABLE public.user_subscription
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , user_uuid UUID NOT NULL
  , subscription_id INT REFERENCES public.subscription(id) NOT NULL
  , order_uuid UUID REFERENCES public.order(uuid) NOT NULL
  , status_id INT REFERENCES public.user_subscription_status(id) NOT NULL
  , expire_date TIMESTAMP NOT NULL
  , modify_date TIMESTAMP NOT NULL DEFAULT now()
  , modify_reason TEXT NOT NULL DEFAULT 'init'
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);