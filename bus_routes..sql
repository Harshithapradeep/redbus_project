-- Create a database for bus_routes table
CREATE database if not EXISTS `redbus` ;

drop table if exists redbus.bus_routes;

-- Create table bus_routes to store data scraped from selenium 
create table redbus.bus_routes(
id INT primary key auto_increment,
route_name TEXT,
route_link TEXT,
busname	TEXT,
bustype	TEXT,
departing_time TIME,
duration TEXT,
reaching_time TIME,
star_rating	FLOAT,
price DECIMAL(10,2),
seats_available	INT,
rtc_name TEXT
);

-- Displays all records

select * from redbus.bus_routes 
