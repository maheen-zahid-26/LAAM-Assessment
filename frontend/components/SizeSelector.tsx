import type { Variant } from "@/lib/types";

interface SizeSelectorProps {
  variants: Variant[];
  selectedSize: string | null;
  onSelect: (size: string) => void;
}

export function SizeSelector({ variants, selectedSize, onSelect }: SizeSelectorProps) {
  return (
    <div>
      <p className="font-mono text-[11px] tracking-[0.18em] text-ink/50 uppercase mb-2">
        Select size
      </p>
      <div className="flex flex-wrap gap-2" role="group" aria-label="Size">
        {variants.map((variant) => {
          const isSelected = variant.size === selectedSize;
          const isEmpty = variant.stock_qty === 0;
          return (
            <button
              key={variant.size}
              type="button"
              onClick={() => onSelect(variant.size)}
              aria-pressed={isSelected}
              className={[
                "font-mono text-sm px-3.5 py-2 rounded-tag border transition-colors",
                isSelected
                  ? "border-teal bg-teal text-paper-raised"
                  : "border-line bg-paper-raised text-ink hover:border-ink/40",
                isEmpty && !isSelected ? "opacity-40" : "",
              ].join(" ")}
            >
              {variant.size}
            </button>
          );
        })}
      </div>
    </div>
  );
}
