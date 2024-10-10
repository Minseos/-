# 시간 포멧
# %H 24시간 표기, %h 12시간 표기, %p AM,PM 표시)
# %i 2자리 분 표기
# %S 2자리 초
# %T 24시간 표기법 시:분:초
# %r 12시간 표기법 시:분:초 AM/PM
# %W 요일의 영문표기, %w 숫자로 요일 표기
select date_format('2024-06-01 19:22:30', '%p %H : %i : %S');
select date_format('2024-06-01 19:22:30', '%h : %i : %S');
select date_format('2024-06-01 19:22:30', '%T');
select date_format('2024-06-01 19:22:30', '%W');

# str_to_date('문자열', '출력 포멧')
select str_to_date('21,01,2021', '%d, %m, %Y');
select str_to_date('19:30:17', '%H:%i:%s');
select str_to_date('19:30:17', '%h:%i:%s');

# sysdate() 현재 날짜와 시간 반환
select sysdate(), sleep(2), sysdate();
select now(), sleep(2), now();

# 현재 날짜를 기준으로 현재 일이 속한 월의 마지막 날짜에
# 해당하는 요일을 구하는 쿼리를 작성하세요.
select curdate();
select last_day(curdate());
select dayname(last_day(curdate()));

# 형 변환 함수 : 형 변환 데이터 타입을 변환하는 함수
# char() char 타입으로 변환
# signed() 정수형(int)로 변환
# decimal() decimal(숫자)으로 변환
# double() double형으로 변환
# float() float 타입으로 변환
# date() date 타입으로 변환
# datetime() datetime 타입으로 변환
# CAST(값 as 변환할 데이터 타입)

select cast(10 as char);						# char() char 타입으로 변환
select cast('-10' as signed);					# signed() 정수형(int)로 변환
select cast('10.1234' as decimal);				# 정수로 변환
select cast('10.1234' as decimal(6,4));			# 자릿수를 정하면 실수로 나옴
select cast('10.1234' as double);				# double() double형으로 변환		
select cast('2021-10-31' as date);				# date() date 타입으로 변환	
select cast('2021-10-31' as datetime);			# datetime() datetime 타입으로 변환

# convert(값, 변환할 타입)
select convert(10, char);						# char() char 타입으로 변환
select convert('-10', signed);					# signed() 정수형(int)로 변환
select convert('10.1234', decimal);				# 정수로 변환
select convert('10.1234', decimal(6,4));			# 자릿수를 정하면 실수로 나옴
select convert('10.1234', double);				# double() double형으로 변환		
select convert('2021-10-31', date);				# date() date 타입으로 변환	
select convert('2021-10-31', datetime);			# datetime() datetime 타입으로 변환

# 연습문제
# 출력 컬럼 이름을 concat으로 합쳐서 출력하기
use world;
# world의 country 테이블에서 인구가 4500만명 - 5500만명 사이에 있는 국가 조회
# code, name, continent, region, population
# name(continent)
select * from country;

select code, concat(name,'(',continent,')'), continent, region, population
from country
where population between 45000000 and 55000000;
