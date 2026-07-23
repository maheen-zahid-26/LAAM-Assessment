import Link from "next/link";

export default function ProductNotFound() {
  return (
    <div className="max-w-md mx-auto px-6 py-24 text-center">
      <p className="font-mono text-[11px] tracking-[0.18em] text-ink/40 uppercase mb-2">
        404
      </p>
      <h1 className="font-display text-2xl mb-2">We couldnt find that product</h1>
      <p className="text-sm text-ink/60 mb-6">
        It may have been removed, or the link might be incorrect.
      </p>
      <Link
        href="/"
        className="font-mono text-sm text-teal underline underline-offset-4"
      >
        Back to catalog
      </Link>
    </div>
  );
}
