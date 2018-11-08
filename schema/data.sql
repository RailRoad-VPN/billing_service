TRUNCATE public.service CASCADE;
TRUNCATE public.service_type CASCADE;
TRUNCATE public.user_service_status CASCADE;
TRUNCATE public.order_status CASCADE;
TRUNCATE public.order CASCADE;
TRUNCATE public.payment_status CASCADE;
TRUNCATE public.order_payment CASCADE;
TRUNCATE public.user_service CASCADE;

-- VPN service service type
INSERT INTO public.service_type (id, name) VALUES (1, 'VPN Subscription');

-- FREE VPN SUBSCRIPTION
INSERT INTO public.service (id, name, price, old_price, billed_period, type_id) VALUES (1, 'Free Pack', 0, 0, 1, 1);
-- STARTER VPN SUBSCRIPTION
INSERT INTO public.service (id, name, price, old_price, billed_period, type_id) VALUES (2, 'Starter Pack', 7.96, 7.96, 1, 1);
-- PRO VPN SUBSCRIPTION
INSERT INTO public.service (id, name, price, old_price, billed_period, type_id) VALUES (3, 'Pro Pack', 6.35, 7.57, 12, 1);
-- ULTIMATE VPN SUBSCRIPTION
INSERT INTO public.service (id, name, price, old_price, billed_period, type_id) VALUES (4, 'Ultimate Pack', 4.25, 5.35, 36, 1);

INSERT INTO public.payment_type (id, name) VALUES (1, 'test');

INSERT INTO public.order_status (id, name) VALUES (1, 'new');
INSERT INTO public.order_status (id, name) VALUES (2, 'processing');
INSERT INTO public.order_status (id, name) VALUES (3, 'success');
INSERT INTO public.order_status (id, name) VALUES (4, 'failed');

INSERT INTO public.payment_status (id, name) VALUES (1, 'success');
INSERT INTO public.payment_status (id, name) VALUES (2, 'failed');
INSERT INTO public.payment_status (id, name) VALUES (3, 'processing');

INSERT INTO public.user_service_status (id, name) VALUES (1, 'active');
INSERT INTO public.user_service_status (id, name) VALUES (2, 'inactive');
INSERT INTO public.user_service_status (id, name) VALUES (3, 'expired');
INSERT INTO public.user_service_status (id, name) VALUES (4, 'waiting for payment');

INSERT INTO public."order" (uuid, code, status_id) VALUES ('fbd762d8-fbb5-4625-969e-398cf3e24274', 1, 3);
INSERT INTO public.order_payment (uuid, order_uuid, type_id, status_id, json_data) VALUES ('34bd42e9-aadd-4eab-8038-c272f38ea48a', 'fbd762d8-fbb5-4625-969e-398cf3e24274', 1, 1, '{"test": "123"}');

INSERT INTO public.user_service (uuid, user_uuid, service_id, order_uuid, status_id, expire_date) VALUES ('e99cb69c-1ddf-47e2-9558-abf6ad83a7b9', 'cf402144-0c02-4b97-98f2-73f7b56160cf', 1, 'fbd762d8-fbb5-4625-969e-398cf3e24274', 1, '2020-06-13 22:26:48.036000');
