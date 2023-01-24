drop table if exists Service_Reservation;
drop table if exists Charging_stations_booking;
drop table if exists Charging_stations;
drop table if exists Customer_Sales;
drop table if exists Customer;
drop table if exists Vendor_Transactions;
drop table if exists Vendor;
drop table if exists Vehicle_Item;
drop table if exists Electric_Vehicle;
drop table if exists Company;


create table Company (
company_id integer primary key,
company_name varchar(64) not null,
email varchar(64) ,
phone_no bigint not null,
city varchar(64)  
);

create table Electric_Vehicle (
ev_vehicle_code integer primary key,
ev_name varchar(64) not null,
ev_range integer not null,
ev_type varchar(64) not null,
launch_year integer not null,
c_id integer not null,
foreign key (c_id) references Company(company_id)
);

create table Vehicle_Item (
item_code integer primary key,
item_name varchar(64) not null,
purchase_price integer not null,
sale_price integer not null,
is_vendor boolean not null,
curr_stock integer not null,
Ev_code integer not null,
Foreign key (ev_code) references Electric_Vehicle(ev_vehicle_code)
);

Create table Vendor (
Vendor_code integer primary key,
Vendor_name varchar(64) not null,
Phone_number bigint not null,
Address varchar(64),
City varchar(32)
);

Create table Vendor_Transactions (
Transaction_code integer primary key,
Transaction_date date not null,
Transaction_desc varchar(64),
V_code integer not null,
It_code integer not null ,
Foreign key (v_code) references Vendor(vendor_code),
Foreign key (it_code) references Vehicle_item(item_code)
);

create table Customer (
customer_id integer primary key,
name varchar(64) not null,
email varchar(64) ,
phone_no bigint not null,
city varchar(64)
);

Create table Customer_Sales (
Sales_code integer primary key,
sales_date date  not null,
sales_desc varchar(64),
C_id integer not null,
It_code integer not null,
Foreign key (C_id) references Customer(customer_id),
Foreign key (it_code) references Vehicle_item(item_code)
);

create table Charging_Stations (
code integer primary key,
location varchar(64) unique not null,
Status boolean not null,
vehicle_type varchar(64) not null  
);

create table Charging_Stations_Booking (
Booking_id integer primary key,
c_code integer not null,
c_id integer not null,
Booking_time timestamp not null,
Foreign key (c_code) references Charging_stations(code),
Foreign key (c_id) references Customer(customer_id)
);

Create table Service_Reservation (
Reserve_id integer,
reserve_date date not null,
Num_days integer not null,
Pickup_date date not null,
Return_date date,
Pickup_location varchar(32),
C_id integer not null,
Primary key(reserve_id, c_id),
Foreign key (c_id) references Customer(customer_id) on delete cascade
);