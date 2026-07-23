interface LoadingSkeletonProps {
  lines?: number;
  className?: string;
}

export function LoadingSkeleton({ lines = 2, className = "" }: LoadingSkeletonProps) {
  return (
    <div className={`animate-pulse space-y-2 ${className}`} aria-live="polite" aria-busy="true">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-3 rounded-tag bg-ink/10"
          style={{ width: i === lines - 1 ? "60%" : "100%" }}
        />
      ))}
      <span className="sr-only">Loading</span>
    </div>
  );
}
