-- Run after schema.sql. Uses fixed UUIDs so they're easy to reference
-- directly in the frontend (e.g. /product/11111111-1111-1111-1111-111111111101).

-- ============ PRODUCTS ============

insert into products (id, title, brand, category, base_price, image_url) values
  ('11111111-1111-1111-1111-111111111101', 'Embroidered Lawn Suit — 3 Piece', 'Sana Safinaz', 'lawn', 8500, 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1'),
  ('11111111-1111-1111-1111-111111111102', 'Printed Lawn Kurta', 'Khaadi', 'lawn', 4200, 'https://images.unsplash.com/photo-1595777457583-95e059d581b8'),
  ('11111111-1111-1111-1111-111111111103', 'Digital Print Lawn Set', 'Gul Ahmed', 'lawn', 5600, 'https://images.unsplash.com/photo-1617019114583-affb34d1b3cd'),
  ('11111111-1111-1111-1111-111111111104', 'Chikankari Lawn Shirt', 'Bareeze', 'lawn', 6100, 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1'),

  ('11111111-1111-1111-1111-111111111105', 'Formal Silk Kurta', 'Khaadi', 'formal', 9800, 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35'),
  ('11111111-1111-1111-1111-111111111106', 'Embellished Formal Gown', 'Elan', 'formal', 24500, 'https://images.unsplash.com/photo-1595777457583-95e059d581b8'),
  ('11111111-1111-1111-1111-111111111107', 'Organza Formal Shirt', 'Sana Safinaz', 'formal', 11200, 'https://images.unsplash.com/photo-1551803091-e20673f15770'),
  ('11111111-1111-1111-1111-111111111108', 'Velvet Formal Suit', 'Maria B', 'formal', 21000, 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d'),

  ('11111111-1111-1111-1111-111111111109', 'Leather Khussa — Handcrafted', 'Stoneage', 'footwear', 3200, 'https://images.unsplash.com/photo-1560343090-f0409e92791a'),
  ('11111111-1111-1111-1111-111111111110', 'Embroidered Mules', 'Insignia', 'footwear', 2800, 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2'),
  ('11111111-1111-1111-1111-111111111111', 'Formal Loafers', 'Borjan', 'footwear', 4500, 'https://images.unsplash.com/photo-1449505278894-297fdb3edbc1'),
  ('11111111-1111-1111-1111-111111111112', 'Casual Sandals', 'Ndure', 'footwear', 1900, 'https://images.unsplash.com/photo-1603487742131-4160ec999306'),

  ('11111111-1111-1111-1111-111111111113', 'Beaded Clutch', 'Zara Shahjahan', 'accessories', 3600, 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7'),
  ('11111111-1111-1111-1111-111111111114', 'Kundan Jewelry Set', 'Ayesha Ibrahim', 'accessories', 7200, 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a'),
  ('11111111-1111-1111-1111-111111111115', 'Silk Dupatta', 'Khaadi', 'accessories', 2100, 'https://images.unsplash.com/photo-1601924994987-69e26d50dc26');

-- ============ VARIANTS (deliberately mixed stock: 0 / low / healthy) ============

-- Lawn (S, M, L, XL)
insert into product_variants (product_id, size, stock_qty) values
  ('11111111-1111-1111-1111-111111111101', 'S', 12), ('11111111-1111-1111-1111-111111111101', 'M', 2), ('11111111-1111-1111-1111-111111111101', 'L', 0), ('11111111-1111-1111-1111-111111111101', 'XL', 8),
  ('11111111-1111-1111-1111-111111111102', 'S', 15), ('11111111-1111-1111-1111-111111111102', 'M', 10), ('11111111-1111-1111-1111-111111111102', 'L', 6), ('11111111-1111-1111-1111-111111111102', 'XL', 1),
  ('11111111-1111-1111-1111-111111111103', 'S', 0), ('11111111-1111-1111-1111-111111111103', 'M', 0), ('11111111-1111-1111-1111-111111111103', 'L', 3), ('11111111-1111-1111-1111-111111111103', 'XL', 9),
  ('11111111-1111-1111-1111-111111111104', 'S', 7), ('11111111-1111-1111-1111-111111111104', 'M', 5), ('11111111-1111-1111-1111-111111111104', 'L', 11), ('11111111-1111-1111-1111-111111111104', 'XL', 4);

-- Formal (S, M, L, XL)
insert into product_variants (product_id, size, stock_qty) values
  ('11111111-1111-1111-1111-111111111105', 'S', 9), ('11111111-1111-1111-1111-111111111105', 'M', 3), ('11111111-1111-1111-1111-111111111105', 'L', 0), ('11111111-1111-1111-1111-111111111105', 'XL', 6),
  ('11111111-1111-1111-1111-111111111106', 'S', 0), ('11111111-1111-1111-1111-111111111106', 'M', 1), ('11111111-1111-1111-1111-111111111106', 'L', 0), ('11111111-1111-1111-1111-111111111106', 'XL', 2),
  ('11111111-1111-1111-1111-111111111107', 'S', 14), ('11111111-1111-1111-1111-111111111107', 'M', 12), ('11111111-1111-1111-1111-111111111107', 'L', 10), ('11111111-1111-1111-1111-111111111107', 'XL', 7),
  ('11111111-1111-1111-1111-111111111108', 'S', 5), ('11111111-1111-1111-1111-111111111108', 'M', 0), ('11111111-1111-1111-1111-111111111108', 'L', 2), ('11111111-1111-1111-1111-111111111108', 'XL', 8);

-- Footwear (sizes as numeric strings)
insert into product_variants (product_id, size, stock_qty) values
  ('11111111-1111-1111-1111-111111111109', '38', 6), ('11111111-1111-1111-1111-111111111109', '39', 0), ('11111111-1111-1111-1111-111111111109', '40', 4), ('11111111-1111-1111-1111-111111111109', '41', 9),
  ('11111111-1111-1111-1111-111111111110', '38', 2), ('11111111-1111-1111-1111-111111111110', '39', 3), ('11111111-1111-1111-1111-111111111110', '40', 0), ('11111111-1111-1111-1111-111111111110', '41', 0),
  ('11111111-1111-1111-1111-111111111111', '38', 11), ('11111111-1111-1111-1111-111111111111', '39', 7), ('11111111-1111-1111-1111-111111111111', '40', 5), ('11111111-1111-1111-1111-111111111111', '41', 3),
  ('11111111-1111-1111-1111-111111111112', '38', 0), ('11111111-1111-1111-1111-111111111112', '39', 0), ('11111111-1111-1111-1111-111111111112', '40', 0), ('11111111-1111-1111-1111-111111111112', '41', 1);

-- Accessories (single size)
insert into product_variants (product_id, size, stock_qty) values
  ('11111111-1111-1111-1111-111111111113', 'One Size', 6),
  ('11111111-1111-1111-1111-111111111114', 'One Size', 0),
  ('11111111-1111-1111-1111-111111111115', 'One Size', 20);

-- ============ PRICE ADJUSTMENTS ============
-- Mix: some products with a discount + fee, some with only one, one with none (product 111...104 gets none).

insert into price_adjustments (product_id, label, type, amount, is_percentage) values
  ('11111111-1111-1111-1111-111111111101', 'Summer Sale', 'discount', 10, true),
  ('11111111-1111-1111-1111-111111111101', 'Delivery fee', 'fee', 150, false),

  ('11111111-1111-1111-1111-111111111102', 'Clearance', 'discount', 500, false),

  ('11111111-1111-1111-1111-111111111103', 'Delivery fee', 'fee', 150, false),

  ('11111111-1111-1111-1111-111111111105', 'Eid Sale', 'discount', 15, true),
  ('11111111-1111-1111-1111-111111111105', 'Delivery fee', 'fee', 200, false),

  ('11111111-1111-1111-1111-111111111106', 'Cash on delivery fee', 'fee', 100, false),

  ('11111111-1111-1111-1111-111111111109', 'Festive Discount', 'discount', 5, true),

  ('11111111-1111-1111-1111-111111111113', 'Bundle Discount', 'discount', 300, false),
  ('11111111-1111-1111-1111-111111111113', 'Delivery fee', 'fee', 100, false);

-- ============ DELIVERY ZONES ============
-- Covers major cities as serviceable; Gilgit-Baltistan explicitly marked
-- NOT serviceable; anything outside these prefixes has no match at all —
-- both "unavailable" paths are exercised deliberately.

insert into delivery_zones (pincode_prefix, min_days, max_days, is_serviceable) values
  ('54', 2, 4, true),   -- Lahore
  ('75', 3, 5, true),   -- Karachi
  ('44', 2, 4, true),   -- Islamabad
  ('60', 3, 6, true),   -- Multan
  ('15', 5, 9, false);  -- Gilgit-Baltistan — explicitly not serviceable
