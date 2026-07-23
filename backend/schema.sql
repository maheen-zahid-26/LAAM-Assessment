-- Run this in the Supabase SQL editor (or via psql) before seed.sql

create extension if not exists pgcrypto; -- for gen_random_uuid()

create table if not exists products (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  brand text not null,
  category text not null,
  base_price numeric not null,
  image_url text,
  created_at timestamptz default now()
);

create table if not exists product_variants (
  id uuid primary key default gen_random_uuid(),
  product_id uuid references products(id) on delete cascade,
  size text not null,
  stock_qty int not null default 0,
  unique(product_id, size)
);

create table if not exists price_adjustments (
  id uuid primary key default gen_random_uuid(),
  product_id uuid references products(id) on delete cascade,
  label text not null,
  type text check (type in ('discount','fee')) not null,
  amount numeric not null,
  is_percentage boolean default false
);

create table if not exists delivery_zones (
  id uuid primary key default gen_random_uuid(),
  pincode_prefix text not null,
  min_days int not null,
  max_days int not null,
  is_serviceable boolean default true
);

create index if not exists idx_variants_product on product_variants(product_id);
create index if not exists idx_adjustments_product on price_adjustments(product_id);
create index if not exists idx_zones_prefix on delivery_zones(pincode_prefix);
