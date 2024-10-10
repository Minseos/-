use world;
show tables;
desc city;
desc country;
desc countrylanguage;

select *
from city;

#다른 데이터베이스에 있는걸 보고 싶을 때
select *
from mywork.highschool_students;

select *
from city where countrycode = "KOR";

# 한국에서 K로 시작하는거
select *
from city
where countrycode = "KOR" and district LIKE("K%");

# district 중간에  ong가 들어가는 자료 찾기
select *
from city
where countrycode = "KOR" and district LIKE("%ong%");

# district 'seoul' ,'kyouggi' in사용
select *
from city
where countrycode = "KOR" and district in("seoul", "kyonggi");


select *
from country;

# country 테이블에서 population이 100,000,000초과인 나라를 찾아보세요
select *
from country
where population > 100000000;

# 우리나라 인구 찾기
select *
from country
where name = "south korea";

# 우리나라 인구와 비슷한 나라 찾기 45,000,000 >= 55,000,000
select *
from country
where population between 45000000 and 55000000;

#-------------------------------------------------------------
# 박스 오피스 데이터 조회
use mywork;
desc box_office;

select * 
from box_office limit 5;

# release_date가 2018-01-01 ~ 2018-12-31 개봉한 rep_country = 한국
#여러개 있는 값들 중에 유일값만 찾아줌
select distinct rep_country from box_office;

select * 
from box_office
where release_date >= "2018-01-01" and release_date <= "2018-12-31";

select * 
from box_office
where release_date between "2018-01-01" and "2018-12-31";

#2019년에 개봉한 영화중 관객이 audiunce_num 1000만 이상인 영화
select *
from box_office where release_date
between '2019-1-1' and '2019-12-31' and audience_num >= 10000000;

use world;
select *
from country;

# order by로 정렬하기
# world 인구가 country 테이블에서 인구가 1억을 초과하는 나라를 추출하고 인구순으로 내림차순
select *
from country
where population > 100000000
order by population desc;

# 조회된 데이터를 2개 컬럼을 기준으로 정렬하기
# 인구수가 5000만명 이상인 나라를 찾아서 continent, region을 기준으로 오름차순 정렬하기
select *
from country
where population > 50000000
order by continent, region asc;
# continent는 내림차순, region은 오름차순
select *
from country
where population > 50000000
order by continent desc, region asc;







































