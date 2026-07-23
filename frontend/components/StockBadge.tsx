import type { StockStatus } from "@/lib/types";

const CONFIG: Record<StockStatus, { label: string; color: string; dot: string }> = {
  in_stock: { label: "In stock", color: "text-sage", dot: "bg-sage" },
  low_stock: { label: "Only a few left", color: "text-amber", dot: "bg-amber" },
  out_of_stock: { label: "Out of stock", color: "text-clay", dot: "bg-clay" },
};

interface StockBadgeProps {
  status: StockStatus;
  stockQty?: number;
}

export function StockBadge({ status, stockQty }: StockBadgeProps) {
  const config = CONFIG[status];
  return (
    <span className={`inline-flex items-center gap-1.5 font-mono text-xs ${config.color}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${config.dot}`} aria-hidden="true" />
      {config.label}
      {status === "low_stock" && typeof stockQty === "number" && (
        <span className="text-ink/40">({stockQty} left)</span>
      )}
    </span>
  );
}
