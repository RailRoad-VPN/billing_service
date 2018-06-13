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
DROP TABLE IF EXISTS public.order_status CASCADE;
DROP TABLE IF EXISTS public.order CASCADE;
DROP TABLE IF EXISTS public.payment_type CASCADE;
DROP TABLE IF EXISTS public.payment CASCADE;
DROP TABLE IF EXISTS public.ppg_payment CASCADE;
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

CREATE TABLE public.payment
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , type_id INT REFERENCES public.payment_type(id) NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.order_status
(
    id SERIAL PRIMARY KEY
  , name VARCHAR(100)
);

CREATE TABLE public.order
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , code INT NOT NULL
  , status_id INT REFERENCES public.order_status(id) NOT NULL
  , payment_uuid UUID REFERENCES public.payment(uuid)
  , modify_date TIMESTAMP NOT NULL DEFAULT now()
  , modify_reason TEXT NOT NULL DEFAULT 'init'
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.user_subscription
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , user_uuid UUID NOT NULL
  , subscription_id INT REFERENCES public.subscription(id) NOT NULL
  , order_uuid UUID REFERENCES public.order(uuid) NOT NULL
  , expire_date TIMESTAMP NOT NULL
  , modify_date TIMESTAMP NOT NULL DEFAULT now()
  , modify_reason TEXT NOT NULL DEFAULT 'init'
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE public.ppg_payment
(
    id SERIAL PRIMARY KEY
  , payment_id INT REFERENCES public.payment_type(id) NOT NULL
  , order_id BIGINT UNIQUE
  , product_id BIGINT
  , order_status VARCHAR(300)
  , order_status_id INT
  , order_referrer_url VARCHAR(300)
  , customer_name VARCHAR(300)
  , customer_first_name VARCHAR(300)
  , customer_last_name VARCHAR(300)
  , customer_email VARCHAR(300)
  , customer_country_name VARCHAR(300)
  , customer_state_name VARCHAR(300)
  , ec_product_id BIGINT
  , product_quantity INT
  , order_item_id BIGINT
  , order_item_name VARCHAR(300)
  , order_item_type_id BIGINT
  , order_item_type_name VARCHAR(300)
  , order_item_sku VARCHAR(300)
  , order_currency_code VARCHAR(50)
  , order_item_vendor_amount NUMERIC
  , order_item_price NUMERIC
  , order_item_unit_price NUMERIC
  , order_item_total_amount NUMERIC
  , order_item_affiliate_amount NUMERIC
  , order_item_partners_amount NUMERIC
  , order_total_amount NUMERIC
  , order_taxes_amount NUMERIC
  , order_item_coupon_discount NUMERIC
  , order_item_dynamic_discount NUMERIC
  , order_item_lead_discount NUMERIC
  , order_item_promo_discount NUMERIC
  , order_item_volume_discount NUMERIC
  , order_item_total_discount NUMERIC
  , order_total_amount_shown NUMERIC
  , vendor_balance_currency_code VARCHAR(50)
  , payment_method_id INT
  , payment_method_name VARCHAR(300)
  , customer_id BIGINT
  , customer_country_code_by_ip VARCHAR(300)
  , customer_country_name_by_ip VARCHAR(300)
  , customer_country_code VARCHAR(300)
  , customer_phone VARCHAR(300)
  , customer_language_code VARCHAR(300)
  , customer_state_code VARCHAR(300)
  , customer_city VARCHAR(300)
  , customer_street_address VARCHAR(300)
  , customer_zipcode VARCHAR(300)
  , corporate_purchase VARCHAR(300)
  , subscription_id BIGINT
  , paypal_account VARCHAR(300)
  , ipn_type_id BIGINT
  , ipn_type_name VARCHAR(300)
  , test_mode INT
  , hash VARCHAR(300)
  , order_items_count VARCHAR(300)
  , regional_price NUMERIC
  , invoice_link VARCHAR(300)
  , credit_card_bin VARCHAR(300)
  , credit_card_last4 VARCHAR(300)
  , credit_card_expiration_date VARCHAR(300)
  , credit_card_bin_result VARCHAR(300)
  , order_total_amount_with_taxes_shown VARCHAR(300)
  , is_delayed_payment INT
  , created_date TIMESTAMP NOT NULL DEFAULT now()
);