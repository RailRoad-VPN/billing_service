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
INSERT INTO public.service (id, name, price, old_price, billed_period, type_id, is_free, is_trial, trial_period_days) VALUES (1, 'Free VPN Pack', 0.00, 0.00, 1, 1, TRUE, FALSE, NULL);
-- PAID VPN SUBSCRIPTION
INSERT INTO public.service (id, name, price, old_price, billed_period, type_id, is_free, is_trial, trial_period_days) VALUES (2, 'VPN Pack', 3.00, 4.00, 1, 1, FALSE, TRUE, 3);

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
