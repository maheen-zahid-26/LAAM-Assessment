'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { getAlternatives } from '@/lib/api';
import type { Alternative } from '@/lib/types';
import { LoadingSkeleton } from './LoadingSkeleton';
import { StitchDivider } from './StitchDivider';

interface AlternativesGridProps {
  productId: string;
  excludeSize: string;
}

function formatPKR(amount: number) {
  return `Rs ${Math.round(amount).toLocaleString('en-PK')}`;
}

export function AlternativesGrid({
  productId,
  excludeSize,
}: AlternativesGridProps) {
  const [items, setItems] = useState<Alternative[] | null>(null);

  // Reset stale items during render when inputs change, instead of in an effect.
  const currentKey = `${productId}:${excludeSize}`;
  const [key, setKey] = useState(currentKey);
  if (key !== currentKey) {
    setKey(currentKey);
    setItems(null);
  }

  useEffect(() => {
    let cancelled = false;
    getAlternatives(productId, excludeSize).then((data) => {
      if (!cancelled) setItems(data);
    });
    return () => {
      cancelled = true;
    };
  }, [productId, excludeSize]);

  if (items && items.length === 0) return null;

  return (
    <section className="mt-8">
      <StitchDivider label="This size isn't available — try instead" />
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-4">
        {items === null &&
          Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="border border-line rounded-tag p-3">
              <LoadingSkeleton lines={2} />
            </div>
          ))}

        {items?.map((item) => (
          <Link
            key={item.id}
            href={`/product/${item.id}`}
            className="border border-line rounded-tag p-3 bg-paper-raised hover:border-teal transition-colors block"
          >
            <div className="relative aspect-3/4 bg-paper rounded-tag overflow-hidden mb-2">
              {item.image_url && (
                <Image
                  src={item.image_url}
                  alt={item.title}
                  fill
                  sizes="200px"
                  className="object-cover"
                />
              )}
            </div>
            <p className="font-mono text-[11px] text-ink/50 uppercase tracking-wide">
              {item.brand}
            </p>
            <p className="text-sm text-ink leading-snug mt-0.5">{item.title}</p>
            <p className="font-mono text-sm text-ink mt-1">
              {formatPKR(item.price)}
            </p>
          </Link>
        ))}
      </div>
    </section>
  );
}
