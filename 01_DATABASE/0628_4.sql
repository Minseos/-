create database naver_db;
use naver_db;

create table member(
mem_id char(8) Not null primary key,
mem_name VARCHAR(10) not null,
mem_number tinyint not null,
addr char(2) not null,
phone1 char(3) null,
phone2 char(8) null,
height tinyint unsigned null,
debut_Date date null
);

create table buy(
num int not null primary key auto_increment,
mem_id char(8) not null ,
prod_name char(8) not null,
group_name char(4) null,
price int unsigned not null,
amount smallint unsigned null,
foreign key(mem_id) references member(mem_id)
);

drop table buy;

alter table buy(
num int not
);

insert into member 
values('TWC', '트와이스', 9, '서울', 02, '11111111', 167, '2015.10.19'),
('BLK', '블랙핑크', 4, '경남', 055, '22222222', 163, '2016.08.08'),
('WMN', '여자친구', 5, '경기', 031, '33333333', 166, '2015.01.15'),
('GRL', '소녀시대', 8, '서울', 02, '44444444', 168, '2007.08.02'),
('RED', '레드벨벳', 4, '경북', 054, '55555555', 161, '2014.08.01'),
('APN', '에이핑크', 6, '경기', 031, '77777777', 164, '2011.02.10'),
('SPC', '우주소녀', 13, '서울', 02, '88888888', 162, '2016.02.25'),
('MMU', '마마무', 4, '전남', 061, '99999999', 165, '2014.06.19');

insert into member (mem_id, mem_name, mem_number, addr, height, debut_date)
values('OMY', '오마이걸', 7, '서울', 160, '2015.04.21'),
('ITZ', '잇지', 5, '경남', 167, '2019.02.12');

select * from member;

insert into buy(num, mem_id, prod_name, price, amount)
values(1, 'BLK', '지갑', 30, 2),
(10, 'MMU', '지갑', 30, 1),
(12, 'MMU', '지갑', 30, 4);

insert into buy values
(2, 'BLK', '맥북프로', '디지털', 1000, 1),
(3, 'APN', '아이폰', '디지털', 200, 1),
(4, 'MMU', '아이폰', '디지털', 200, 5),
(5, 'BLK', '청바지', '패션', 50, 3),
(6, 'MMU', '에어팟', '디지털', 80, 10),
(7, 'GRL', '혼공SQL', '서적', 15, 5),
(8, 'APN', '혼공SQL', '서적', 15, 2),
(9, 'APN', '청바지', '패션', 50, 1),
(11, 'APN', '혼공SQL', '서적', 15, 1);

select * from buy;

select *
from member as m inner join buy as b
on m.mem_id = b.mem_id;

select *
from member as m left join buy as b
on m.mem_id = b.mem_id;

select *
from member as m right join buy as b
on m.mem_id = b.mem_id;


# 서브쿼리
# 쿼리 안에 또 다들 쿼리를 이용해서 원하는 데이터를
# 이름이 에이핑크인 회원의 평균키(height)보다 큰 회원을 조회하기
select * from member
where mem_name = '에이핑크';

select mem_name, height
from member
where height > (select hieght from member
where mem_name = '에이핑크');


















