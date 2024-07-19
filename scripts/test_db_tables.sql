select * from device_registry;
select * from measurements;

insert into device_registry (mac_address, ip_address, device_type, description, registered_at, updated_at)
values ('ed:b7:b1:a1:e6:c0', '58.34.215.253', 'test_device_type', 'test_description', current_timestamp, current_timestamp)
on conflict (mac_address) do update
set updated_at = excluded.updated_at;

insert into measurements (time, device_id, sensor_tag, value)
values (current_timestamp, 3, 'test_sensor2', 200);