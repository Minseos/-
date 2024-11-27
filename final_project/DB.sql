CREATE TABLE `Store` (
  `store_id` integer PRIMARY KEY,
  `store_name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `category` varchar(255),
  `phone_number` varchar(255),
  `business_hours` varchar(255),
  `price_range` varchar(255),
  `naver_rating` decimal(2,1),
  `kakao_rating` decimal(2,1),
  `google_rating` decimal(2,1)
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

ALTER TABLE `Review` ADD FOREIGN KEY (`store_id`) REFERENCES `Store` (`store_id`);
