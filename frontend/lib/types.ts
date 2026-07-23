export type StockStatus = 'in_stock' | 'low_stock' | 'out_of_stock';

export interface Variant {
  size: string;
  stock_qty: number;
}

export interface PriceLine {
  label: string;
  amount: number;
}

export interface PriceBreakdown {
  base_price: number;
  discounts: PriceLine[];
  fees: PriceLine[];
  final_price: number;
}

export interface ProductSummary {
  id: string;
  title: string;
  brand: string;
  category: string;
  base_price: number;
  image_url: string | null;
}

export interface Product {
  id: string;
  title: string;
  brand: string;
  category: string;
  base_price: number;
  image_url: string | null;
  variants: Variant[];
  price_breakdown: PriceBreakdown;
}

export interface Availability {
  size: string;
  stock_qty: number;
  status: StockStatus;
}

export interface DeliveryEstimateResult {
  serviceable: true;
  min_days: number;
  max_days: number;
  estimated_date: string;
}

export interface DeliveryUnavailable {
  serviceable: false;
  message: string;
}

export type DeliveryEstimate = DeliveryEstimateResult | DeliveryUnavailable;

export interface Alternative {
  id: string;
  title: string;
  brand: string;
  price: number;
  image_url: string | null;
  size_available: boolean;
}
