SELECT count(*)
FROM korea_exchange_rate.exchange_rate_1995_2024;
# 292761

SELECT *
FROM korea_exchange_rate.exchange_rate_1995_2024
where date = '2003-10-20';
# 2003-10-20~21 중복

SELECT *
FROM korea_exchange_rate.exchange_rate_1995_2024
where date = '2003-10-17';