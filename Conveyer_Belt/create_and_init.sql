create table category(
    id int not null auto_increment,
    name varchar(16),
    ko_name varchar(16),
    constraint pk_category primary key(id),
    constraint uq_name_category unique(name)
);

create table section(
	id int not null auto_increment,
	name varchar(16),
	category_id int,  -- section의 category_id는 nullable (입고장은 category가 없음)
	constraint pk_section primary key(id),
	constraint uq_name_section unique(name),
	constraint fk_section foreign key(category_id)
		references category(id)
		on update cascade on delete cascade
);

create table rfid(
	id int not null auto_increment,
	uid varchar(16),
	in_time timestamp, -- 커넥션 시간대 기준으로 UTC를 조회하여 UTC 값 저장
    out_time timestamp,
    tag_info varchar(128),
    category_id int,
    now_section int,
    section_update_time timestamp on update current_timestamp,
	constraint pk_rfid primary key(id),
	constraint uq_uid_rfid unique(uid),
	constraint fk_category_id_rfid foreign key(category_id)
		references category(id)
		on update cascade on delete cascade,
    constraint fk_now_section_rfid foreign key(now_section)  -- foreign key는 null값도 가능, insert시에는 null로
        references section(id)
        on update cascade on delete cascade  -- 부모 테이블 레코드 update/delete 시, 해당 레코드를 참조하는 자식 테이블 레코드도 update/delete
);

create table belt(
	id int not null auto_increment,
	activated boolean,
	speed int,
	last_activated_time timestamp,
	constraint pk_belt primary key(id)
);

create table car(
	id int not null auto_increment,
	isLineDriving boolean,
	isAutoDriving boolean,
	isManualDriving boolean,
	pos POINT,
	departedAt timestamp,
	arrivedAt timestamp,
	constraint pk_car primary key(id)
);

create table warning_log(
	id int not null auto_increment,
	belt_id int,
	car_id int,
	log_time timestamp default current_timestamp,
	log_message text,
	constraint pk_warning_log primary key(id),
	constraint fk_belt_id_warning_log foreign key(belt_id)
		references belt(id)
		on update cascade on delete cascade,
	constraint fk_car_id_warning_log foreign key(car_id)
		references car(id)
		on update cascade on delete cascade
);

create table car_log(
	id int not null auto_increment,
	car_id int,
	log_time timestamp default current_timestamp,
	log_message text,
	constraint pk_car_log primary key(id),
	constraint fk_car_id_car_log foreign key(car_id)
		references car(id)
		on update cascade on delete cascade
);


insert into category (name) values
	('seoul_storage'),
	('busan_storage'),
	('outgoing');

insert into section (name, category_id) values
	('receiving', NULL),
	('slide_1', 1),
	('slide_2', 2),
	('drop', 3);

insert into rfid (uid, category_id) values
	('C3 B4 D1 0D', 1),
	('23 42 CE 0D', 2),
	('23 49 CE 0D', 3),
	('53 B3 B7 0D', 1),
	('33 E9 BF 0D', 2),
	('33 F7 D3 0D', 3),
	('73 A9 B5 0D', 1),
	('63 AE BE 0D', 2);