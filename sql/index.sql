create index idx_frame_info on frame_raw using gin (info);
create index idx_frame_atom on frame_raw using gin (atom);

create index idx_frame_info_ops on frame_raw using gin (info jsonb_ops);
create index idx_frame_atom_ops on frame_raw using gin (atom jsonb_ops);

create index idx_frame_info_pops on frame_raw using gin (info jsonb_path_ops);
create index idx_frame_atom_pops on frame_raw using gin (atom jsonb_path_ops);

--create index idx_frame_keys on frame_raw using gin (jsonb_object_keys(info));
--create index idx_frame_keys on frame_raw using gin (jsonb_object_keys(atom));

create index idx_frame_total_energy on frame_raw using gin ((info->'total_energy'));
create index idx_frame_config_type on frame_raw using gin ((info->'config_type'));
create index idx_frame_config_name on frame_raw using gin ((info->'config_name'));

