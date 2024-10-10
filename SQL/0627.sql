create schema testdb;
create database testdb2;
# testdb3이라는게 없으면 만들어라
create database if not exists testdb3;
Drop database testdb3;
Drop schema testdb2;
drop database if exists testdb;

create database if not exists mywork;

use mywork;
show tables;
select * from student_info;

create database testdb4;
Drop database testdb4;

show databases;
use mywork;
show tables;

drop table student_info;
drop table if exists student_info;

# 식별자 명명 규칙
# 식별자 : 데이터베이스 이름, 테이블 이름, 컬럼명
# 1. 최대길이 64글자까지 가능
# 2. 사용 가능 문자 0~9, 영문자, 한글, $, _를 사용할 수 있다
# 3. 예약어(create, database, avg, show)
# 4. 대소문자 구분(windows는 관계없음), Linux, unix는 대소문자 구분

#컬럼 생성시 주의사항
# 한 테이블에 최대 4096개까지 컬럼을 만들 수 있다.
# 한 테이블에서 같은 컬럼명을 사용할 수 없다.
# 데이터 베이스 내에서 같은 테이블 명도 사용할 수 없다

create database test_db;

# SQL을 사용해서 테이블 만들기 create table
create table highschool_students(
student_no 		varchar(20),
student_name 	varchar(100),
grade 			tinyint,
class 			varchar(50),
gender 			varchar(20),
age 			smallint,
enter_date 		date
);

# 생성한 테이블의 구조를 출력 describe, desc
desc highschool_students;

# 제약조건을 넣어서 만들기 null, not null
create table highschool_students2(
student_no	varchar(20) not null,
student_name varchar(100) not null,
grade tinyint null,
class varchar(50) null,
gender varchar(20) null,
age smallint,
enter_date date
);

desc highschool_students2;
drop table highschool_students;

# 기본키를 포함해서 만들기 (기본키 : primary key)
create table highschool_students
(
student_no varchar(20) not null Primary key,
student_name varchar(100) not null,
grade tinyint null,
class varchar(50) null,
gender varchar(20) null,
age smallint,
enter_date date
);

desc highschool_students;
drop table highschool_students;

create table highschool_students
(
student_no varchar(20) not null,
student_name varchar(100) not null,
grade tinyint null,
class varchar(50) null,
gender varchar(20) null,
age smallint,
enter_date date,
primary key(student_no)
);

desc highschool_students;
drop table highschool_students;

#constraint(제약조건) primary key로 기본키 설정하기
create table highschool_students
(
student_no varchar(20) not null,
student_name varchar(100) not null,
grade tinyint null,
class varchar(50) null,
gender varchar(20) null,
age smallint,
enter_date date,
constraint primary key(student_no)
);

desc highschool_students;

# 기본키 primary key 삭제하기 alter drop
# alter는 만들어진 데이터베이스나 테이블을 수정할 대 사용하는 명령어
alter table highschool_students
drop primary key;

desc highschool_students;

# 기본키 추가하기 alter add
alter table highschool_students add primary key(student_no);
desc highschool_students;

# 기본키 생성시 주의사항
# 1. 한 테이블에서 기본키는 1개만 생성할 수 있다.
# 1개 이상의 컬럼으로 기본키를 생성할 수 있다.
# 기본 키 컬럼에는 not null을 적용한다.


use mywork;

select count(*) from box_office;
select count(*) from employees;
select count(*) from departments;
select count(*) from dept_manager;
select count(*) from dept_emp;
select count(*) from titles;
select count(*) from salaries;





























