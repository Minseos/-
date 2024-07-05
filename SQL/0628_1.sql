create database testdb;
use testdb;
create table testtable(
student_no int not null primary key,
student_name varchar(100)  not null,
grade tinyint,
class varchar(50),
gender varchar(20),
age smallint,
enter_date date
);

desc testtable;

# 테이블에 데이터를 입력 insert into
# insert into `테이블명(컬럼명)` values(값)
insert into `testtable`(
student_no, student_name, grade, class, gender, age, enter_date)
values(1, '홍길동', 1, '1반', '남자', 20, '2024-03-02');

# 순서가 바뀌어도 values에서 순서를 맞줘서 넣어주면 상관없음
insert into `testtable`(
student_no, grade, class, student_name, gender, age, enter_date)
values(2, 1, '1반','홍길동', '남자', 20, '2024-03-02');

select * from testtable;

insert into `testtable`(
student_no, grade, class, student_name, gender, age, enter_date)
values(3, 1, '1반','홍길동', '남자', 20, '2024-03-02'),
(4, 1, '1반','홍길동', '남자', 20, '2024-03-02'),
(5, 1, '1반','홍길동', '남자', 20, '2024-03-02'),
(6, 1, '1반','홍길동', '남자', 20, '2024-03-02');

select * from testtable;
