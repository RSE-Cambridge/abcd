CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "hstore";

begin;
drop table if exists frame_raw cascade;

create table frame_raw (
  frame_id uuid primary key default uuid_generate_v1(),
  info jsonb,
  atom jsonb
);
commit;
