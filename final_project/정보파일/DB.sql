CREATE TABLE `Store` (
  `store_id` integer PRIMARY KEY,
  `store_name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `category` varchar(255),
  `phone_number` varchar(255),
  `business_hours` varchar(255),
  `price_range` varchar(255),
  `naver_rating` float,
  `kakao_rating` float,
  `google_rating` float
);

CREATE TABLE `Review` (
  `review_id` integer PRIMARY KEY,
  `store_id` integer NOT NULL,
  `platform` varchar(255) NOT NULL,
  `review_date` date NOT NULL,
  `review_text` text NOT NULL,
  `final_sentiment` enum(긍정적,부정적,알 수 없음) NOT NULL,
  `taste` enum(긍정적,부정적,알 수 없음) NOT NULL,
  `service` enum(긍정적,부정적,알 수 없음) NOT NULL,
  `quantity` enum(긍정적,부정적,알 수 없음) NOT NULL,
  `sentiment` enum(긍정적,부정적,알 수 없음) NOT NULL,
  `sentiment2` enum(긍정적,부정적,알 수 없음) NOT NULL
);

CREATE TABLE `Analysis` (
  `store_id` integer PRIMARY KEY,
  `menu_photo` text,
  `wordcloud` text,
  `negative_ratio` text,
  `distribution` text,
  `keyword` text,
  `raderchart` text
);

ALTER TABLE `Review` ADD FOREIGN KEY (`store_id`) REFERENCES `Store` (`store_id`);

ALTER TABLE `Analysis` ADD FOREIGN KEY (`store_id`) REFERENCES `Store` (`store_id`);
