"use client";

import { useState } from "react";
import { useDeliveryEstimate } from "@/hooks/useDeliveryEstimate";
import { LoadingSkeleton } from "./LoadingSkeleton";
import { ErrorState } from "./ErrorState";

interface DeliveryEstimateProps {
  productId: string;
}

export function DeliveryEstimate({ productId }: DeliveryEstimateProps) {
  const [pincode, setPincode] = useState("");
  const { data, loading, error } = useDeliveryEstimate(productId, pincode);

  return (
    <div>
      <label htmlFor="pincode" className="font-mono text-[11px] tracking-[0.18em] text-ink/50 uppercase mb-2 block">
        Check delivery — enter pincode
      </label>
      <input
        id="pincode"
        type="text"
        inputMode="numeric"
        value={pincode}
        onChange={(e) => setPincode(e.target.value.replace(/[^\d]/g, ""))}
        placeholder="e.g. 54000"
        maxLength={6}
        className="w-full max-w-35 font-mono text-sm border border-line bg-paper-raised rounded-tag px-3 py-2 focus:border-teal"
      />

      <div className="mt-2 min-h-6">
        {pincode.length > 0 && pincode.length < 4 && (
          <p className="text-sm text-ink/40">Enter a full pincode to check.</p>
        )}

        {loading && <LoadingSkeleton lines={1} className="max-w-55" />}

        {!loading && error && <ErrorState message={error} />}

        {!loading && !error && data && data.serviceable && (
          <p className="text-sm text-sage">
            Arrives in {data.min_days}–{data.max_days} days · est.{" "}
            <span className="font-mono">{data.estimated_date}</span>
          </p>
        )}

        {!loading && !error && data && !data.serviceable && (
          <p className="text-sm text-clay">{data.message}</p>
        )}
      </div>
    </div>
  );
}
