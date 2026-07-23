"use client";

import { useState } from "react";
import Image from "next/image";
import type { Product } from "@/lib/types";
import { useAvailability } from "@/hooks/useAvailability";
import { SizeSelector } from "./SizeSelector";
import { StockBadge } from "./StockBadge";
import { PriceBreakdown } from "./PriceBreakdown";
import { DeliveryEstimate } from "./DeliveryEstimate";
import { AlternativesGrid } from "./AlternativesGrid";
import { StitchDivider } from "./StitchDivider";
import { LoadingSkeleton } from "./LoadingSkeleton";
import { ErrorState } from "./ErrorState";

interface ProductViewProps {
  product: Product;
}

export function ProductView({ product }: ProductViewProps) {
  const [selectedSize, setSelectedSize] = useState<string | null>(null);
  const { data: availability, loading: availabilityLoading, error: availabilityError } =
    useAvailability(product.id, selectedSize);

  const canAddToBag = availability?.status === "in_stock" || availability?.status === "low_stock";

  return (
    <div className="max-w-5xl mx-auto px-6 py-10 grid md:grid-cols-2 gap-10">
      <div className="relative aspect-4/5 bg-paper-raised border border-line rounded-tag overflow-hidden">
        {product.image_url && (
          <Image
            src={product.image_url}
            alt={product.title}
            fill
            sizes="(min-width: 768px) 480px, 100vw"
            className="object-cover"
            priority
          />
        )}
      </div>

      <div>
        <p className="font-mono text-[11px] tracking-[0.18em] text-ink/50 uppercase">
          {product.brand}
        </p>
        <h1 className="font-display text-3xl leading-tight mt-1 mb-6">{product.title}</h1>

        <div className="space-y-5">
          <StitchDivider label="Size & fit" />
          <SizeSelector
            variants={product.variants}
            selectedSize={selectedSize}
            onSelect={setSelectedSize}
          />

          <div className="min-h-6">
            {!selectedSize && (
              <p className="text-sm text-ink/40">Select a size to check availability.</p>
            )}
            {selectedSize && availabilityLoading && <LoadingSkeleton lines={1} className="max-w-40" />}
            {selectedSize && !availabilityLoading && availabilityError && (
              <ErrorState message={availabilityError} />
            )}
            {selectedSize && !availabilityLoading && availability && (
              <StockBadge status={availability.status} stockQty={availability.stock_qty} />
            )}
          </div>

          <StitchDivider label="Price" />
          <PriceBreakdown breakdown={product.price_breakdown} />

          <StitchDivider label="Delivery" />
          <DeliveryEstimate productId={product.id} />

          <button
            type="button"
            disabled={!canAddToBag}
            className={[
              "w-full mt-4 py-3 rounded-tag font-mono text-sm tracking-wide transition-colors",
              canAddToBag
                ? "bg-teal text-paper-raised hover:bg-teal/90"
                : "bg-ink/10 text-ink/40 cursor-not-allowed",
            ].join(" ")}
          >
            {canAddToBag ? "Add to bag" : "Select an available size"}
          </button>
        </div>

        {selectedSize && availability?.status === "out_of_stock" && (
          <AlternativesGrid productId={product.id} excludeSize={selectedSize} />
        )}
      </div>
    </div>
  );
}
