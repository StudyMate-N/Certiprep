-- CPA private catalogue schema snapshot; media files are not BLOBs.
create schema if not exists cpa_library;
revoke all on schema cpa_library from public, anon, authenticated;
create table if not exists cpa_library.resources (id text primary key, decision text not null, title text not null, record jsonb not null, updated_at timestamptz not null default now());
create table if not exists cpa_library.assets (path text primary key, sha256 text not null check(length(sha256)=64), bytes bigint not null check(bytes>0), record jsonb not null, updated_at timestamptz not null default now());
create table if not exists cpa_library.audit_events (event_key text primary key, event_type text not null, record jsonb not null, created_at timestamptz not null default now());
create table if not exists cpa_library.settings (key text primary key, value jsonb not null, updated_at timestamptz not null default now());
alter table cpa_library.resources enable row level security;
alter table cpa_library.assets enable row level security;
alter table cpa_library.audit_events enable row level security;
alter table cpa_library.settings enable row level security;
revoke all on all tables in schema cpa_library from public, anon, authenticated;
