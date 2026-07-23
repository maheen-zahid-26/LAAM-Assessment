interface StitchDividerProps {
  label: string;
}

export function StitchDivider({ label }: StitchDividerProps) {
  return (
    <div className="flex items-center gap-3 py-1" role="separator" aria-label={label}>
      <span className="font-mono text-[11px] tracking-[0.18em] text-ink/50 uppercase shrink-0">
        {label}
      </span>
      <div className="stitch-line flex-1" aria-hidden="true" />
    </div>
  );
}
