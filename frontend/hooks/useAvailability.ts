'use client';

import { useEffect, useState } from 'react';
import { getAvailability } from '@/lib/api';
import type { Availability } from '@/lib/types';

interface State {
  data: Availability | null;
  loading: boolean;
  error: string | null;
}

export function useAvailability(productId: string, size: string | null) {
  const [state, setState] = useState<State>({
    data: null,
    loading: false,
    error: null,
  });

  // Reset/seed state during render when inputs change, not synchronously in the effect.
  const currentKey = `${productId}:${size}`;
  const [key, setKey] = useState(currentKey);
  if (key !== currentKey) {
    setKey(currentKey);
    setState({ data: null, loading: !!size, error: null });
  }

  useEffect(() => {
    if (!size) return;

    let cancelled = false;

    getAvailability(productId, size)
      .then((data) => {
        if (!cancelled) setState({ data, loading: false, error: null });
      })
      .catch((err) => {
        if (!cancelled) {
          setState({
            data: null,
            loading: false,
            error: err?.message ?? "Couldn't check stock for this size.",
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [productId, size]);

  return state;
}
