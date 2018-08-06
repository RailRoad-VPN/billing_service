TRUNCATE public.subscription  CASCADE;
TRUNCATE public.subscription_translation CASCADE;
TRUNCATE public.subscription_feature CASCADE;
TRUNCATE public.subscription_feature_translation CASCADE;
TRUNCATE public.payment_type CASCADE;
TRUNCATE public.order_status CASCADE;
TRUNCATE public."order" CASCADE;
TRUNCATE public.order_payment CASCADE;
TRUNCATE public.user_subscription CASCADE;


-- subscriptions (1 - FREE, 2 - STARTER, 3 - PRO, 4 - ULTIMATE

-- FREE
INSERT INTO public.subscription (id, price_per_month, old_price_per_month, billed_period_in_months, billed_period_in_years) VALUES (1, 0, 0, 1, 0);
INSERT INTO public.subscription_translation (subscription_id, name, description, bill_freq, price_freq, lang_code) VALUES (1, 'FREE PACK', 'Try it for free!', 'not billed', 'not billed', 'en');
INSERT INTO public.subscription_translation (subscription_id, name, description, bill_freq, price_freq, lang_code) VALUES (1, 'Бесплатный ПАК', 'Попробуй бесплатно!', 'не оплачивается', 'не оплачивается', 'ru');

-- STARTER
INSERT INTO public.subscription (id, price_per_month, old_price_per_month, billed_period_in_months, billed_period_in_years) VALUES (2, 8.69, 7.96, 12, 1);
INSERT INTO public.subscription_translation (subscription_id, name, description, bill_freq, price_freq, lang_code) VALUES (2, 'STARTER PACK', 'Good pack to start!', 'billed monthly', 'per month', 'en');
INSERT INTO public.subscription_translation (subscription_id, name, description, bill_freq, price_freq, lang_code) VALUES (2, 'Начальный ПАК', 'Хорошее начало пути!', 'оплачивается ежемесячно', 'в месяц', 'ru');

-- PRO
INSERT INTO public.subscription (id, price_per_month, old_price_per_month, billed_period_in_months, billed_period_in_years, is_best) VALUES (3, 6.35, 7.57, 12, 1, TRUE);
INSERT INTO public.subscription_translation (subscription_id, name, description, bill_freq, price_freq, lang_code) VALUES (3, 'PRO PACK', 'We know what you need', 'billed yearly', 'per month', 'en');
INSERT INTO public.subscription_translation (subscription_id, name, description, bill_freq, price_freq, lang_code) VALUES (3, 'Профессиональный ПАК', 'Мы знаем, что вам нужно!', 'оплачивается ежегодно', 'в месяц', 'ru');


-- ULTIMATE
INSERT INTO public.subscription (id, price_per_month, old_price_per_month, billed_period_in_months, billed_period_in_years) VALUES (4, 4.25, 5.35, 36, 3);
INSERT INTO public.subscription_translation (subscription_id, name, description, bill_freq, price_freq, lang_code) VALUES (4, 'ULTIMATE PACK', 'You know what you want!', 'billed every 3 years', 'per month', 'en');
INSERT INTO public.subscription_translation (subscription_id, name, description, bill_freq, price_freq, lang_code) VALUES (4, 'Максимальный ПАК', 'Ты знаешь, что тебе нужно!', 'оплачивается раз в 3 года', 'в месяц', 'ru');

-- ULTIMATE PACK
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (1,  4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (2,  4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (3,  4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (4,  4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (5,  4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (6,  4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (7,  4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (8,  4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (9,  4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (10, 4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (11, 4, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (12, 4, TRUE);
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (1,  'ALL Countries', 'Number of countries where you can choose VPN server', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (1,  'Все Страны', 'Количество стран, в которых вы можете выбрать VPN сервер', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (2,  '10 Devices', 'Number of devices (laptop, smartphone, tablet) where you can connect VPN at once time', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (2,  '10 Устройств', 'Количество устройств (ноутбук, смартфон, планшет) на которых можно подключить VPN в один момент времени', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (3,  'Speed: Highest', 'Your connection will be on Highest speed', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (3,  'Скорость: Максимальная', 'Скорость вашего соединегния будет Максимальной', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (4,  'No Browsing Logs Policy', 'We do not collect logs about your connection, which means you can browse the internet without any worry of being recorded', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (4,  'Нет браузерной истории логов', 'Мы не собираем никакой информации о вашем подключении и трафике', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (5,  'Virus Protection', NULL, 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (5,  'Защита от Вирусов', NULL, 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (6,  'Fast Connect', 'VPN client connects automatically to the fastest server available within few seconds', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (6,  'Моментальное соединение', 'Наш VPN клиент автоматически соединяется с быстрейшим сервером за несколько секунд', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (7,  'Full support', 'Write us any time with any problem about Railroad Network', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (7,  'Полная поддержка', 'Пиши нам в любое время по любой проблеме о работае сервиса Railroad Network', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (8,  'Military Grade 256-Bit Encryption', 'Our servers use advanced 256-bit encryption to offer best protection for you', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (8,  'Военный стандарт 256 битного шифрования', 'Наши сервера используют продвинутое 256 битное шифрование, чтобы предложить вам наилучшую защиту', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (9,  'Advanced IPSec & IKEv2 protocols', 'We support multiple VPN security protocols for you to choose from to fulfill your needs and requirements', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (9,  'Продвинутые IPSec & IKEv2 прокотолы', 'Мы поддерживаем несколько VPN протоколов безопасности, чтобы Вы могли выбрать подходящий для себя', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (10, 'Service +', 'Servers only available to VIP users with the highest speed', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (10, 'Сервис +', 'Сервера доступны только для VIP пользователей на максимальной скорости', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (11, 'Streaming Services', 'Watch Netflix, Twitch and Youtube', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (11, 'Стриминговые сервисы', 'Смотрите Ivi, Twitch, Youtube', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (12, 'Torrents and P2P', 'User P2P services, download torrents without restricts or limits ', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (12, 'Торренты и P2P службы', 'Используйте P2P сервисы, скачивайте торренты без ограничений!', 'ru');

-- PRO PACK
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (13, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (14, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (15, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (16, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (17, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (18, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (19, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (20, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (21, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (22, 3, FALSE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (23, 3, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (24, 3, TRUE);
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (13, 'ALL Countries', 'Number of countries where you can choose VPN server', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (13, 'Все Страны', 'Количество стран, в которых вы можете выбрать VPN сервер', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (14, '5 Devices', 'Number of devices (laptop, smartphone, tablet) where you can connect VPN at once time', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (14, '5 Устройств', 'Количество устройств (ноутбук, смартфон, планшет) на которых можно подключить VPN в один момент времени', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (15, 'Speed: High', 'Your connection will be on High speed', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (15, 'Скорость: Высокая', 'Скорость вашего соединегния будет Высокой', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (16, 'No Browsing Logs Policy', 'We do not collect logs about your connection, which means you can browse the internet without any worry of being recorded', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (16, 'Нет браузерной истории логов', 'Мы не собираем никакой информации о вашем подключении и трафике', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (17, 'Virus Protection', NULL, 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (17, 'Защита от Вирусов', NULL, 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (18, 'Fast Connect', 'VPN client connects automatically to the fastest server available within few seconds', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (18, 'Моментальное соединение', 'Наш VPN клиент автоматически соединяется с быстрейшим сервером за несколько секунд', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (19, 'Full support', 'Write us any time with any problem about Railroad Network', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (19, 'Полная поддержка', 'Пиши нам в любое время по любой проблеме о работае сервиса Railroad Network', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (20, 'Military Grade 256-Bit Encryption', 'Our servers use advanced 256-bit encryption to offer best protection for you', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (20, 'Военный стандарт 256 битного шифрования', 'Наши сервера используют продвинутое 256 битное шифрование, чтобы предложить вам наилучшую защиту', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (21, 'Advanced IPSec & IKEv2 protocols', 'We support multiple VPN security protocols for you to choose from to fulfill your needs and requirements', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (21, 'Продвинутые IPSec & IKEv2 прокотолы', 'Мы поддерживаем несколько VPN протоколов безопасности, чтобы Вы могли выбрать подходящий для себя', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (22, 'Service +', 'Servers only available to VIP users with the highest speed', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (22, 'Сервис +', 'Сервера доступны только для VIP пользователей на максимальной скорости', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (23, 'Streaming Services', 'Watch Netflix, Twitch and Youtube', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (23, 'Стриминговые сервисы', 'Смотрите Ivi, Twitch, Youtube', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (24, 'Torrents and P2P', 'User P2P services, download torrents without restricts or limits ', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (24, 'Торренты и P2P службы', 'Используйте P2P сервисы, скачивайте торренты без ограничений!', 'ru');

-- STARTER PACK
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (25, 2, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (26, 2, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (27, 2, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (28, 2, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (29, 2, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (30, 2, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (31, 2, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (32, 2, FALSE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (33, 2, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (34, 2, FALSE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (35, 2, FALSE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (36, 2, FALSE);
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (25, '3 Countries', 'Number of countries where you can choose VPN server', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (25, '3 Страны', 'Количество стран, в которых вы можете выбрать VPN сервер', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (26, '3 Devices', 'Number of devices (laptop, smartphone, tablet) where you can connect VPN at once time', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (26, '3 Устройства', 'Количество устройств (ноутбук, смартфон, планшет) на которых можно подключить VPN в один момент времени', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (27, 'Speed: Low', 'Your connection will be on Low speed', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (27, 'Скорость: Низкая', 'Скорость вашего соединегния будет Низкой', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (28, 'No Browsing Logs Policy', 'We do not collect logs about your connection, which means you can browse the internet without any worry of being recorded', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (28, 'Нет браузерной истории логов', 'Мы не собираем никакой информации о вашем подключении и трафике', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (29, 'Virus Protection', NULL, 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (29, 'Защита от Вирусов', NULL, 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (30, 'Fast Connect', 'VPN client connects automatically to the fastest server available within few seconds', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (30, 'Моментальное соединение', 'Наш VPN клиент автоматически соединяется с быстрейшим сервером за несколько секунд', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (31, 'Limited support', 'Write an email or forum post about your problems, we will help, may be', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (31, 'Ограниченная поддержка', 'Пиши на почту и на форум о всех своих проблемах. Как-чего - мы починим.', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (32, 'Military Grade 256-Bit Encryption', 'Our servers use advanced 256-bit encryption to offer best protection for you', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (32, 'Военный стандарт 256 битного шифрования', 'Наши сервера используют продвинутое 256 битное шифрование, чтобы предложить вам наилучшую защиту', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (33, 'Advanced IPSec & IKEv2 protocols', 'We support multiple VPN security protocols for you to choose from to fulfill your needs and requirements', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (33, 'Продвинутые IPSec & IKEv2 прокотолы', 'Мы поддерживаем несколько VPN протоколов безопасности, чтобы Вы могли выбрать подходящий для себя', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (34, 'Service +', 'Servers only available to VIP users with the highest speed', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (34, 'Сервис +', 'Сервера доступны только для VIP пользователей на максимальной скорости', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (35, 'Streaming Services', 'Watch Netflix, Twitch and Youtube', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (35, 'Стриминговые сервисы', 'Смотрите Ivi, Twitch, Youtube', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (36, 'Torrents and P2P', 'User P2P services, download torrents without restricts or limits ', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (36, 'Торренты и P2P службы', 'Используйте P2P сервисы, скачивайте торренты без ограничений!', 'ru');


-- FREE PACK
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (37, 1, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (38, 1, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (39, 1, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (40, 1, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (41, 1, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (42, 1, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (43, 1, TRUE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (44, 1, FALSE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (45, 1, FALSE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (46, 1, FALSE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (47, 1, FALSE);
INSERT INTO public.subscription_feature (id, subscription_id, enabled) VALUES (48, 1, FALSE);
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (37, '1 Country', 'Number of countries where you can choose VPN server', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (37, '1 Страна', 'Количество стран, в которых вы можете выбрать VPN сервер', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (38, '1 Device', 'Number of devices (laptop, smartphone, tablet) where you can connect VPN at once time', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (38, '1 Устройство', 'Количество устройств (ноутбук, смартфон, планшет) на которых можно подключить VPN в один момент времени', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (39, 'Speed: Minimal', 'Your connection will be on Minimal speed, but you can browse internet and chatting', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (39, 'Скорость: Самая низкая', 'Скорость вашего соединегния будет Самой низкой, но вам хватит на браузер и чаты', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (40, 'No Browsing Logs Policy', 'We do not collect logs about your connection, which means you can browse the internet without any worry of being recorded', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (40, 'Нет браузерной истории логов', 'Мы не собираем никакой информации о вашем подключении и трафике', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (41, 'Virus Protection', NULL, 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (41, 'Защита от Вирусов', NULL, 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (42, 'Fast Connect', 'VPN client connects automatically to the fastest server available within few seconds', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (42, 'Моментальное соединение', 'Наш VPN клиент автоматически соединяется с быстрейшим сервером за несколько секунд', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (43, 'No support', NULL, 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (43, 'Нет поддержки', NULL, 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (44, 'Military Grade 256-Bit Encryption', 'Our servers use advanced 256-bit encryption to offer best protection for you', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (44, 'Военный стандарт 256 битного шифрования', 'Наши сервера используют продвинутое 256 битное шифрование, чтобы предложить вам наилучшую защиту', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (45, 'Advanced IPSec & IKEv2 protocols', 'We support multiple VPN security protocols for you to choose from to fulfill your needs and requirements', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (45, 'Продвинутые IPSec & IKEv2 прокотолы', 'Мы поддерживаем несколько VPN протоколов безопасности, чтобы Вы могли выбрать подходящий для себя', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (46, 'Service +', 'Servers only available to VIP users with the highest speed', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (46, 'Сервис +', 'Сервера доступны только для VIP пользователей на максимальной скорости', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (47, 'Streaming Services', 'Watch Netflix, Twitch and Youtube', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (47, 'Стриминговые сервисы', 'Смотрите Ivi, Twitch, Youtube', 'ru');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (48, 'Torrents and P2P', 'User P2P services, download torrents without restricts or limits ', 'en');
INSERT INTO public.subscription_feature_translation (subscription_feature_id, name, tooltip, lang_code) VALUES (48, 'Торренты и P2P службы', 'Используйте P2P сервисы, скачивайте торренты без ограничений!', 'ru');


INSERT INTO public.payment_type (id, name) VALUES (1, 'payproglobal');
INSERT INTO public.payment_type (id, name) VALUES (2, 'payproglobal_test');

INSERT INTO public.order_status (id, name) VALUES (1, 'new');
INSERT INTO public.order_status (id, name) VALUES (2, 'processing');
INSERT INTO public.order_status (id, name) VALUES (3, 'success');
INSERT INTO public.order_status (id, name) VALUES (4, 'failed');

INSERT INTO public.payment_status (id, name) VALUES (1, 'success');
INSERT INTO public.payment_status (id, name) VALUES (2, 'failed');
INSERT INTO public.payment_status (id, name) VALUES (3, 'processing');

INSERT INTO public.user_subscription_status (id, name) VALUES (1, 'active');
INSERT INTO public.user_subscription_status (id, name) VALUES (2, 'inactive');
INSERT INTO public.user_subscription_status (id, name) VALUES (3, 'expired');
INSERT INTO public.user_subscription_status (id, name) VALUES (4, 'waiting for payment');

INSERT INTO public."order" (uuid, code, status_id) VALUES ('fbd762d8-fbb5-4625-969e-398cf3e24274', 1, 3);
INSERT INTO public.order_payment (uuid, order_uuid, type_id, created_date) VALUES ('34bd42e9-aadd-4eab-8038-c272f38ea48a', 'fbd762d8-fbb5-4625-969e-398cf3e24274', 1, '2018-08-03 17:34:22.704861');

INSERT INTO public.user_subscription (uuid, user_uuid, subscription_id, order_uuid, expire_date) VALUES ('e99cb69c-1ddf-47e2-9558-abf6ad83a7b9', 'cf402144-0c02-4b97-98f2-73f7b56160cf', 2, 'fbd762d8-fbb5-4625-969e-398cf3e24274', '2019-06-13 22:26:48.036000');