-- create device and program registry tables
create table if not exists device_registry (
    device_id int generated always as identity,
    mac_address macaddr not null,
    ip_address cidr not null,
    device_type varchar(255) not null,
    description varchar(255)
);

create table if not exists program_registry (
    program_id int generated always as identity,
    device_id int,
    port int not null,
    description varchar(255)
);

-- fill in the tables with initial info
insert into program_registry (device_id, port, description)
values
    (1, 5431, 'smart-home-timescaledb, postgres extension for time series data'),
    (1, 5432, 'smart-home-postgres, postgres for devices used in house');
