begin;

drop type if exists frame_info cascade;
drop type if exists atom_info cascade;
drop view if exists frame;
drop view if exists atoms;

--create type frame_info as (total_energy real, config_type text);

--create view frame as
--select frame_id, (jsonb_populate_record(null::frame_info, info)).* from frame_raw;

--create type atom_info as (number integer, position real[3], force real[3]);

--create view atoms as
--select frame_id, (jsonb_populate_record(null::atom_info, info)).* from frame_raw;

--create or replace view frame_keys as select count(*), jsonb_object_keys(info) as key from frame_raw group by key;

drop view if exists frame_keys;
create view frame_keys as 
select count(*), key, jsonb_typeof(info->key) as key_type
from (
  select frame_id, info, jsonb_object_keys(info) as key
  from frame_raw
) x
where key=key
group by key, key_type;

drop view if exists atom_keys;
create view atom_keys as
select count(*), key, jsonb_typeof(atom->key) as key_type
from (
  select frame_id, atom, jsonb_object_keys(atom) as key
  from frame_raw
) x
where key=key
group by key, key_type;

commit;
