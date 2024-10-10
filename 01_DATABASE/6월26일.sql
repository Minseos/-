show databases;
use titanic;

# p_info Name 컬럼의 값에서 Braund라는 이름을 갖는 사람 찾기
SELECT * FROM p_info
WHERE Name = "Braund";
#안나옴

SELECT * FROM p_info
WHERE Name Like('Braund%');

SELECT * FROM p_info
WHERE Name Like('%Mrs%');

SELECT * FROM p_info
WHERE Name not Like("%Mrs");

#in 안에 있는 값이 있는 경우 가져오기
#SibSP가 4,5,6인 경우
SELECT * from p_info
WHERE SibSp = 4 or SibSp = 5 or SibSp = 6;

SELECT * FROM p_info
where SibSp in(4,5,6);

#not in
select * from p_info where sibSP not in(4,5,6);

#between a and b = a이상 b이하
#p_info Age가 40이상, 60이하인 사람을 검색하세요.
SELECT * FROM p_info
WHERE Age between 40 and 60; 

#is null/is not null(결측치, 값이 없음)
#Age 컬럼에서 NULL이 있는지 찾기
SELECT * FROM p_info WHERE Age is NULL;

#--------------------------------------------------------
#t_info 테이블에서 Fare가 100 이상 1000이하인 승객을 조회하시오.
#and 사용
SELECT * FROM t_info
WHERE Fare >= 100 and Fare <= 1000;

#between 사용
SELECT * FROM t_info
WHERE Fare between 100 and 1000;

#t_info 테이블에서 Tickert이 PC로 시작하고 Embarked가 C 혹은 S인 승객을 조회하시오.
SELECT * FROM t_info
WHERE Ticket Like("PC%") and Embarked IN("C", "S");

SELECT * FROM t_info
WHERE Ticket Like("PC%") and Embarked =("C" or "S");

#t_info 테이블에서 Pclass가 1 혹은 2인 승객을 조회하시오.
#OR
SELECT * FROM t_info
WHERE Pclass = 1 or Pclass = 2;

#in
SELECT * FROM t_info
WHERE Pclass in(1,2);

#t_info 테이블에서 Cabin에 숫자 59가 포함된 승객을 조회하시오.
SELECT * FROM t_info
WHERE Cabin Like('%59%');

#p_info 테이블에서 Age가 NULL이 아니면서 이름에 James가 포함된 40세 이상의 남성을 조회하시오
SELECT * FROM p_info
WHERE Age IS NOT NULL and Name LIKE("%James%") and Age >= 40 and Sex = "male";

#select * from 테이블명 where 컬럼명 order by 기준 컬럼명 ASC(오름차순)/DESC(내림차순)
#p_info 테이블에서 age가 null이 아니면서 이름에 miss가 포함된 40세 이하의 여성을 조회하고 나이순으로 내림차순 정렬
SELECT * FROM p_info
WHERE Age IS NOT NULL and Name Like("%miss%") and Age <= 40 and Sex = "female" order by age desc;


#p_info 테이블에서 나이가 null이 아닌 행의 성별별 나이 평균을 구하시오
#age is not null, sex
SELECT sex, AVG(age)
FROM p_info
WHERE age IS NOT NULL group by sex; 

SELECT sex, AVG(age), MIN(age), MAX(age)
FROM p_info
WHERE age IS NOT NULL group by sex; 

SELECT SibSp, AVG(age), MIN(age), MAX(age)
FROM p_info
WHERE age IS NOT NULL group by SibSp; 

# having : group by 한 결과에서 원하는 조건에 맞는 결과만 다시 추릴 때. where
# t_info 테이블에서 pclass별 fare 가격 평균을 구하고 그 중 가격 평균이 50을 초과하는 결과만 조회
#pclass별 fare 가격 평균 : group by pclass avg(fare)
select * from t_info;


select Pclass, avg(fare)
from t_info
group by Pclass having avg(fare) > 50;


#inner join(교집합) 기준 컬럼을 비교해 양쪽에 데이터가 있는 행만 합쳐줌
select * from passenger;
select * from ticket;

#passenger, ticket의 inner join
select p.PassengerId, Name
from passenger as p inner join ticket as t on p.PassengerId = t.PassengerId;

select *
from passenger as p inner join ticket as t on p.PassengerId = t.PassengerId;

#left join
select *
from passenger as p left join ticket as t on p.PassengerId = t.PassengerId;

#right join
select * from passenger as p right join ticket as t on p.PassengerId = t.PassengerId;

#full outer join : mysql에서 지원 X, union이란 명령어로 left join 결과와 right join 결과를 합침
SELECT *
FROM passenger as p left join ticket as t on p.PassengerId = t.PassengerId
union
select *
from passenger as p right join ticket as t on p.PassengerId = t.PassengerId; 

#원하는 컬럼만 조회하기 : 컬럼명을 그대로 적어준다. 단, 컬럼명이 중복되면 약칭(별칭)을 사용해서 어느 테이블인지 명시한다.
select p.passengerId, p.name, p.age, t.Pclass, p.Embarked
from passenger as p
left join ticket as t
on p.PassengerId = t.PassengerId;

# 3개 이상의 테이블 조인하기
# passenger, ticket, survived inner join 합쳐서 전체 컬럼을 출력하시오
select *
from passenger as p
inner join ticket as t
on p.PassengerId = t.PassengerId
inner join survived as s
on t.PassengerId = s.PassengerId;


#1. passenger, ticket, survived 테이블을 조인하고 Survived가 1인 사람들만 찾아서 Name, Age, Sex, Pclass, survived 컬럼을 출력하시오.
select name, age, sex, Pclass, survived
from passenger as p
inner join ticket as t
on p.PassengerId = t.PassengerId
inner join survived as s
on t.PassengerId = s.PassengerId
where s.Survived = 1;


#2. 1의 결과를 10개만 출력하시오.
select name, age, sex, Pclass, survived
from passenger as p
inner join ticket as t
on p.PassengerId = t.PassengerId
inner join survived as s
on t.PassengerId = s.PassengerId
where s.Survived = 1 limit 10;

#3. Passenger 테이블을 기준으로  ticket, survived 테이블을 LEFT JOIN 한 결과에서 성별이 여성이면서 Pclass가 1인 사람 중 생존자를 찾아 이름, 성별, Pclass를 표시하시오.
select name, sex, Pclass
from passenger as p
left join ticket as t
on p.PassengerId = t.PassengerId
left join survived as s
on p.PassengerId = s.PassengerId
where Sex = "female" and Pclass = 1 and s.Survived = 1;

#4. Passenger, ticket, survived 테이블을 left join 후 나이가 10세 이상 20세 이하 이면서 Pclass 2인 사람 중 생존자를 표시하시오.
select *
from Passenger as p left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where age between 10 and 20 and Pclass = 2 and survived = 1;


#5. Passenger, ticket, survived 테이블을 left join 후 성별이 여성 또는 Pclass 가 1인 사람 중 생존자를 표시하시오.
select *
from Passenger as p left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where (sex = "female" or Pclass = 1) and (survived = 1);


#6. Passenger, ticket, survived 테이블을 left join 후 생존자 중에서 이름에 Mrs가 포함된 사람을 찾아 이름, Pclass, 나이, Parch, Survived 를 표시하시오.
select Pclass, age, Parch, survived
from Passenger as p left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where name Like("%Mrs%") and survived = 1;

#7. Passenger, ticket, survived 테이블을 left join 후 Pclass가 1, 2이고 Embarked가 s, c 인 사람중에서 생존자를 찾아 이름, 성별, 나이를 표시하시오.
select name, sex, age
from passenger as p 
left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where (Pclass in(1,2) and Embarked in("s","c")) and survived = 1;

#8. Passenger, ticket, survived 테이블을 left join 후 이름에 James가 들어간 사람중 생존자를 찾아 이름, 성별, 나이 를 표시하고 나이를 기준으로 내림차순 정렬하시오.
select name, sex, age
from passenger as p 
left join ticket as t on p.PassengerId = t.PassengerId
left join survived as s on p.PassengerId = s.PassengerId
where name Like('%James%') and survived = 1 order by age desc;

#9. Passenger, ticket, survived 테이블을 INNER JOIN한 데이터에서 성별별, 생존자의 숫자를 구하시오. 생존자 숫자 결과는 별칭을 Total로 하시오.
select sex, count(Survived) as Total
from passenger as p 
inner join ticket as t on p.PassengerId = t.PassengerId
inner join survived as s on p.PassengerId = s.PassengerId
where survived = 1
group by sex;

#10. Passenger, ticket, survived 테이블을 INNER JOIN한 데이터에서 성별별, 생존자의 숫자, 생존자 나이의 평균을 구하시오. 생존자 숫자 결과는 별칭을 Total로 하시오.
select sex, count(Survived) as Total, avg(age)
from passenger as p 
inner join ticket as t on p.PassengerId = t.PassengerId
inner join survived as s on p.PassengerId = s.PassengerId
where survived = 1
group by sex;
























