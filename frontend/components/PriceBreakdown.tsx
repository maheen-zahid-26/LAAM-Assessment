import type { PriceBreakdown as PriceBreakdownType } from "@/lib/types";

interface PriceBreakdownProps {
  breakdown: PriceBreakdownType;
}

function formatPKR(amount: number) {
  return `Rs ${Math.round(amount).toLocaleString("en-PK")}`;
}

export function PriceBreakdown({ breakdown }: PriceBreakdownProps) {
  const { base_price, discounts, fees, final_price } = breakdown;

  return (
    <div className="border border-line bg-paper-raised rounded-tag tag-perforated pt-4 px-4 pb-3">
      <div className="flex items-baseline justify-between font-mono text-sm text-ink/70">
        <span>Base price</span>
        <span>{formatPKR(base_price)}</span>
      </div>

      {discounts.map((d) => (
        <div
          key={d.label}
          className="flex items-baseline justify-between font-mono text-sm text-teal mt-1"
        >
          <span>{d.label}</span>
          <span>-{formatPKR(d.amount)}</span>
        </div>
      ))}

      {fees.map((f) => (
        <div
          key={f.label}
          className="flex items-baseline justify-between font-mono text-sm text-ink/70 mt-1"
        >
          <span>{f.label}</span>
          <span>+{formatPKR(f.amount)}</span>
        </div>
      ))}

      <div className="stitch-line my-3" aria-hidden="true" />

      <div className="flex items-baseline justify-between">
        <span className="font-mono text-[11px] tracking-[0.18em] text-ink/50 uppercase">
          You pay
        </span>
        <span className="font-display text-3xl text-ink">{formatPKR(final_price)}</span>
      </div>
    </div>
  );
}
