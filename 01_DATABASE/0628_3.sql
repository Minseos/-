# CRUD 연습
use mywork;
create table emp_test(
emp_no int not null,
emp_name varchar(30) not null,
hire_date date null,
salary int null,
primary key(emp_no)
);

desc emp_test;

insert into `emp_test`
values(1005, '퀴리', '2021-03-01', 4000),
(1006, '호킹', '2021-03-05', 5000),
(1007, '패러데이', '2021-04-01', 2200),
(1008, '맥스웰', '2021-04-05', 3300),
(1009, '플랑크', '2021-04-05', 4400);

select * from emp_test; 

insert into `emp_test` (emp_no, emp_name, hire_date)
values(1005, '퀴리', '2021-03-01'),
(1003, '갈릴레이', '2021-02-10');

# 테이블 데이터 수정하기
# update 테이블 set 컬럼1 = 값, 컬럼2 = 값 where 찾을 값
update emp_test
set salary = 50
where emp_no = 1003;

update emp_test
set salary = 10000;

update emp_test
set salary = 1000
where emp_no = 1001;

update emp_test
set salary = null
where emp_no = 1002;

update emp_test
set salary = null
where emp_no = 1003;

update emp_test
set salary = 3000
where emp_no = 1004;

update emp_test
set salary = 4000
where emp_no = 1005;

update emp_test
set salary = 5000
where emp_no = 1006;

update emp_test
set salary = 2200
where emp_no = 1007;

update emp_test
set salary = 3300
where emp_no = 1008;
update emp_test
set salary = 4400
where emp_no = 1009;

select * from emp_test;

# delete 문으로 데이터 삭제하기
# delete from 테이블 where 조건
delete from emp_test;
delete from emp_test 
where emp_no = 1009;

# 트랜잭션 처리하기
# 오토 커밋 옵션 활성화 확인 1 = 활성화, 0 = 비활성화
select @@autocommit;

# 오토 커밋, 설정 set autocommit = 0/1
set autocommit = 0;
select @@autocommit;

select * from emp_test;
create table emp_tran1 as select * from emp_test;

select *
from emp_tran1;

desc emp_tran1;
alter table emp_tran1 add constraint primary key(emp_no);

create table emp_tran2 as select * from emp_test;
select *
from emp_tran2;
desc emp_tran2;
alter table emp_tran2 add constraint primary key(emp_no);

delete from emp_tran1;
select *
from emp_tran1;
commit;
rollback;











