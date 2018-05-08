begin;

drop type if exists frame_info cascade;
drop type if exists atom_info cascade;
drop view if exists frame;
drop view if exists atoms;

create type frame_info as (total_energy real, config_type text);

create view frame as
select frame_id, (jsonb_populate_record(null::frame_info, info)).* from frame_raw;

create type atom_info as (number integer, position real[3], force real[3]);

create view atoms as
select frame_id, (jsonb_populate_record(null::atom_info, info)).* from frame_raw;

create or replace view frame_keys as select count(*), jsonb_object_keys(info) as key from frame_raw group by key;
create or replace view atom_keys as select count(*), jsonb_object_keys(atom) as key from frame_raw group by key;

commit;
