create table if not exists device_registry (
    device_id int generated always as identity,
    mac_address macaddr not null,
    ip_address cidr not null,
    device_type varchar(255) not null,
    description varchar (255),
    registered_at timestamp with time zone default current_timestamp,
    updated_at timestamp with time zone default current_timestamp
);

create table if not exists measurements (
time timestamptz not null,
device_id int not null,
sensor_tag varchar(255) not null,
value float
);

alter table device_registry add constraint unique_id unique (mac_address);

create index on measurements (device_id, sensor_tag, time asc);
select create_hypertable('measurements', by_range('time'));
