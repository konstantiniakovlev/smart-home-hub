create table if not exists device_registry (
    device_id int generated always as identity,
    mac_address macaddr not null,
    ip_address cidr not null,
    device_type varchar(255) not null,
    description varchar(255),
    registered_at timestamp with time zone default current_timestamp,
    updated_at timestamp with time zone default current_timestamp
);

alter table device_registry add constraint unique_id unique (mac_address);


create table if not exists measurements (
time timestamptz not null,
device_id int not null,
sensor_tag varchar(255) not null,
value float
);

create index on measurements (device_id, sensor_tag, time asc);
select create_hypertable('measurements', by_range('time'));


create table if not exists sensors (
    name varchar(255) not null,
    tag varchar(255) not null,
    description varchar(255)
);

alter table sensors add constraint unique_sensor unique (name, tag);

insert into sensors (name, tag, description)
 values ('BM280 Temperature Sensor', 'BME280-TEMP-PV', 'BM280 Temperature Sensor - Processed Value')
  on conflict (name, tag) do
   update set name = excluded.name, tag = excluded.tag, description = excluded.description;

insert into sensors (name, tag, description)
 values ('BM280 Pressure Sensor', 'BME280-PRES-PV', 'BM280 Pressure Sensor - Processed Value')
  on conflict (name, tag) do
   update set name = excluded.name, tag = excluded.tag, description = excluded.description;

insert into sensors (name, tag, description)
 values ('BM280 Humidity Sensor', 'BME280-HUMID-PV', 'BM280 Humidity Sensor - Processed Value')
  on conflict (name, tag) do
   update set name = excluded.name, tag = excluded.tag, description = excluded.description;
