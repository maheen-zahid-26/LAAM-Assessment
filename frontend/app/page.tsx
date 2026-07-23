import Link from 'next/link';
import Image from 'next/image';
import { getProducts } from '@/lib/api';

function formatPKR(amount: number) {
  return `Rs ${Math.round(amount).toLocaleString('en-PK')}`;
}

export default async function Home() {
  let products;
  let loadFailed = false;

  try {
    products = await getProducts();
  } catch (err) {
    console.error('getProducts failed:', err);
    loadFailed = true;
  }

  if (loadFailed || !products) {
    return (
      <div className="max-w-md mx-auto px-6 py-24 text-center">
        <p className="font-mono text-[11px] tracking-[0.18em] text-clay uppercase mb-2">
          Something went wrong
        </p>
        <h1 className="font-display text-2xl mb-2">
          Couldn&apos;t load the catalog
        </h1>
        <p className="text-sm text-ink/60">
          The catalog service may be unavailable right now. Try refreshing the
          page.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <p className="font-mono text-[11px] tracking-[0.18em] text-ink/50 uppercase mb-2">
        LAAM
      </p>
      <h1 className="font-display text-3xl mb-3">Purchase Confidence</h1>

      {products.length === 0 ? (
        <p className="text-sm text-ink/50">No products available right now.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {products.map((product) => (
            <Link
              key={product.id}
              href={`/product/${product.id}`}
              className="border border-line rounded-tag p-3 bg-paper-raised hover:border-teal transition-colors block"
            >
              <div className="relative aspect-3/4 bg-paper rounded-tag overflow-hidden mb-2">
                {product.image_url && (
                  <Image
                    src={product.image_url}
                    alt={product.title}
                    fill
                    sizes="(min-width: 768px) 220px, 45vw"
                    className="object-cover"
                  />
                )}
              </div>
              <p className="font-mono text-[11px] text-ink/50 uppercase tracking-wide">
                {product.brand}
              </p>
              <p className="text-sm text-ink leading-snug mt-0.5">
                {product.title}
              </p>
              <p className="font-mono text-sm text-ink mt-1">
                {formatPKR(product.base_price)}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
