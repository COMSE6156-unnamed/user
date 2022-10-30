CREATE TABLE `user` (
  `user_id` int NOT NULL DEFAULT '0',
  `password` varchar(45) NOT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `id_UNIQUE` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;