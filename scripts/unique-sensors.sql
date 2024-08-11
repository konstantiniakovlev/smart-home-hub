create table if not exists sensors (
    name varchar(255) not null,
    tag varchar(255) not null,
    description varchar(255)
);

alter table sensors add constraint unique_sensor unique (name, tag);


insert into sensors (name, tag, description)
 values ('Soil Moisture Sensor', 'SM_PV', 'AZDelivery Hygrometer Soil Moisture Sensor - raw value')
  on conflict (name, tag) do
  update set name = excluded.name, tag = excluded.tag, description = excluded.description;

insert into sensors (name, tag, description)
 values ('Soil Moisture Sensor Calculated', 'SM_CALC', 'AZDelivery Hygrometer Soil Moisture Sensor - calculated moisture percentage')
  on conflict (name, tag) do
   update set name = excluded.name, tag = excluded.tag, description = excluded.description;
