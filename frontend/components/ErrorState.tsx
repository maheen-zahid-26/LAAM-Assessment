interface ErrorStateProps {
  message: string;
}

export function ErrorState({ message }: ErrorStateProps) {
  return (
    <p className="text-sm text-clay flex items-start gap-1.5" role="alert">
      <span aria-hidden="true">·</span>
      {message}
    </p>
  );
}
