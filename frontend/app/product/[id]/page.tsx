import { notFound } from 'next/navigation';
import { getProduct, ApiError } from '@/lib/api';
import { ProductView } from '@/components/ProductView';

interface ProductPageProps {
  params: Promise<{ id: string }>;
}

export default async function ProductPage({ params }: ProductPageProps) {
  const { id } = await params;

  let product;
  let loadFailed = false;

  try {
    product = await getProduct(id);
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) {
      notFound();
    }
    console.error('getProduct failed:', err); // add this
    loadFailed = true;
  }
  if (loadFailed || !product) {
    // Backend unreachable or 5xx — show a page-level error rather than a blank screen.
    return (
      <div className="max-w-md mx-auto px-6 py-24 text-center">
        <p className="font-mono text-[11px] tracking-[0.18em] text-clay uppercase mb-2">
          Something went wrong
        </p>
        <h1 className="font-display text-2xl mb-2">
          Couldn t load this product
        </h1>
        <p className="text-sm text-ink/60">
          The catalog service may be unavailable right now. Try refreshing the
          page.
        </p>
      </div>
    );
  }

  return <ProductView product={product} />;
}
