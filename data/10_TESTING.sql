-- Новостные ресурсы
INSERT INTO "nf_resources" ("id", "url", "update_interval", "update_datetime", "title", "comment", "parser_id", "source_type_id", "parser_detail_id") VALUES ('5aba81a7-acb7-4cbe-9498-c796845d51c1', 'https://dzen.ru/news', '24:00:00', '2024-08-24 21:10:34.056249', 'Яндекс новости', 'Агрегатор новостей с различных ресурсов', 1, 1, 6);
INSERT INTO "nf_resources" ("id", "url", "update_interval", "update_datetime", "title", "comment", "parser_id", "source_type_id", "parser_detail_id") VALUES ('354d1fce-0a0b-43ab-89b5-945181df3e06', 'https://www.mskagency.ru/lenta?type=text', '24:00:00', NULL, 'Агентсво городских новостей Москва', NULL, NULL, 1, 1);
INSERT INTO "nf_resources" ("id", "url", "update_interval", "update_datetime", "title", "comment", "parser_id", "source_type_id", "parser_detail_id") VALUES ('f0eed543-61ad-4dc3-860c-89e579ac0ea6', 'https://ria.ru/', '00:01:00', '2024-08-25 12:51:58.979768', 'РИА Новости', NULL, 5, 1, 1);


-- Категории новостей на сайте
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('20194cb6-9a3e-4f8b-a6b9-e9ca27a0b0c3', 'Главное', 'https://dzen.ru/news', '5aba81a7-acb7-4cbe-9498-c796845d51c1', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('2a189e02-e679-4a5d-b4fc-d560a8ecf6b6', 'В мире', 'https://dzen.ru/news/rubric/world', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009225', 7, 2, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('54d1e28b-0bb1-46df-9996-1098138afc00', 'Наука', 'https://dzen.ru/news/rubric/science', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009292', 13, 3, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('7f75f9b4-61c5-4a52-9896-08639a52d51b', 'Культура', 'https://dzen.ru/news/rubric/culture', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009281', 11, 3, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('8ff52760-9536-4d00-afdb-87ef8dbd28cc', 'Экономика', 'https://dzen.ru/news/rubric/business', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009217', 5, 3, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('9a4b2602-a074-42d9-9e34-5c5b71bdf8a3', 'СВО', 'https://dzen.ru/news/rubric/svo', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009222', 6, 2, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('9aa19337-4167-41af-914e-9ef94f25cb50', 'Москва', 'https://www.mskagency.ru/lenta?type=text', '354d1fce-0a0b-43ab-89b5-945181df3e06', '00:01:00', '2024-08-25 12:51:59.009303', 15, 4, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('a7ccb6e6-0b61-42c2-8fb7-8880a41e16b5', 'Шоу-бизнес', 'https://dzen.ru/news/rubric/showbusiness', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009259', 9, 2, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('bcc35ac8-266c-404e-8e1d-0cee42ab5185', 'Москва', 'https://dzen.ru/news/region/moscow', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.0093', 15, 2, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('c4c047d8-be94-439a-8945-7fbc6ca98daa', 'Авто', 'https://dzen.ru/news/rubric/auto', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009296', 14, 2, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('c74d28a9-f8de-4328-87d3-782c4e15c777', 'Политика', 'https://dzen.ru/news/rubric/politics', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009204', 3, 3, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('e19ee86b-bc10-45f3-9dff-c22d423efd5d', 'Спорт', 'https://dzen.ru/news/rubric/sport', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009229', 8, 3, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('e8993eb1-35a6-4f07-8c72-e681c5b9ff3f', 'Общество', 'https://dzen.ru/news/rubric/society', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009212', 4, 3, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('fd468436-9eff-4f18-925e-de8d2bfc10b6', 'Технологии', 'https://dzen.ru/news/rubric/computers', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009287', 12, 3, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('063919e0-4dfc-402d-8358-46afdf19beca', 'Интересное', 'https://dzen.ru/news/rubric/personal_feed', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009171', 2, 2, NULL, NULL);
INSERT INTO "nf_remote_categories" ("id", "name", "url", "news_resource_id", "update_interval", "update_datetime", "category_id", "parser_id", "deletion_datetime", "notification_datetime") VALUES ('0d3b90fa-3096-4201-9a93-8443dedcb73a', 'Происшествия', 'https://dzen.ru/news/rubric/incident', '5aba81a7-acb7-4cbe-9498-c796845d51c1', '00:01:00', '2024-08-25 12:51:59.009275', 10, 2, NULL, NULL);

-- Пользователи
INSERT INTO "bot_users" ("user_id") VALUES (2093468718);

-- Роли пользователей
INSERT INTO "bot_user_roles" ("id", "user_id", "role_id") VALUES ('d91100ed-b053-4055-bf07-e5f87a3febaf', 2093468718, 1);

-- Подписки
INSERT INTO "nf_user_subscription" ("id", "user_id", "resource_id", "category_id") VALUES ('86712b25-94a1-41b5-babf-95bb2a394fd4', 2093468718, '5aba81a7-acb7-4cbe-9498-c796845d51c1', 15);


