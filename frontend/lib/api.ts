import type {
  Product,
  ProductSummary,
  Availability,
  DeliveryEstimate,
  Alternative,
} from './types';

const BASE = process.env.NEXT_PUBLIC_API_URL;
console.log('API BASE:', BASE);

if (!BASE && typeof window !== 'undefined') {
  // Surface a clear signal during development rather than failing silently on every call.
  console.warn('NEXT_PUBLIC_API_URL is not set — API calls will fail.');
}

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function handle<T>(res: Response, fallbackMessage: string): Promise<T> {
  if (!res.ok) {
    let message = fallbackMessage;
    try {
      const body = await res.json();
      message = body?.detail ?? fallbackMessage;
    } catch {
      // response wasn't JSON — keep fallback message
    }
    throw new ApiError(message, res.status);
  }
  return res.json();
}

export async function getProducts(): Promise<ProductSummary[]> {
  const res = await fetch(`${BASE}/products`, { cache: 'no-store' });
  return handle<ProductSummary[]>(res, 'Could not load the catalog.');
}

export async function getProduct(id: string): Promise<Product> {
  const res = await fetch(`${BASE}/products/${id}`, { cache: 'no-store' });
  return handle<Product>(res, 'Could not load this product.');
}

export async function getAvailability(
  productId: string,
  size: string,
): Promise<Availability> {
  const res = await fetch(
    `${BASE}/products/${productId}/availability?size=${encodeURIComponent(size)}`,
    { cache: 'no-store' },
  );
  return handle<Availability>(res, "Couldn't check stock for this size.");
}

export async function getDeliveryEstimate(
  productId: string,
  pincode: string,
): Promise<DeliveryEstimate> {
  const res = await fetch(
    `${BASE}/delivery/estimate?pincode=${encodeURIComponent(
      pincode,
    )}&product_id=${productId}`,
    { cache: 'no-store' },
  );
  // Note: the backend returns 200 with serviceable:false for "no coverage here" —
  // that's a valid business outcome, not a request failure. Only network/4xx/5xx throw.
  return handle<DeliveryEstimate>(
    res,
    "Couldn't check delivery for this pincode.",
  );
}

export async function getAlternatives(
  productId: string,
  excludeSize: string,
): Promise<Alternative[]> {
  const res = await fetch(
    `${BASE}/products/${productId}/alternatives?exclude_size=${encodeURIComponent(
      excludeSize,
    )}`,
    { cache: 'no-store' },
  );
  if (!res.ok) return [];
  return res.json();
}

export { ApiError };
