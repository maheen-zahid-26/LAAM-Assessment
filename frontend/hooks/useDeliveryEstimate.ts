'use client';

import { useEffect, useState } from 'react';
import { getDeliveryEstimate } from '@/lib/api';
import type { DeliveryEstimate } from '@/lib/types';

interface State {
  data: DeliveryEstimate | null;
  loading: boolean;
  error: string | null;
}

const DEBOUNCE_MS = 400;
const VALID_PINCODE = /^\d{4,6}$/;

export function useDeliveryEstimate(productId: string, pincode: string) {
  const [state, setState] = useState<State>({
    data: null,
    loading: false,
    error: null,
  });

  // Reset/seed state during render when inputs change, not synchronously in the effect.
  const currentKey = `${productId}:${pincode}`;
  const [key, setKey] = useState(currentKey);
  if (key !== currentKey) {
    setKey(currentKey);
    setState({ data: null, loading: VALID_PINCODE.test(pincode), error: null });
  }

  useEffect(() => {
    if (!VALID_PINCODE.test(pincode)) return;

    let cancelled = false;

    const timer = setTimeout(() => {
      getDeliveryEstimate(productId, pincode)
        .then((data) => {
          if (!cancelled) setState({ data, loading: false, error: null });
        })
        .catch((err) => {
          if (!cancelled) {
            setState({
              data: null,
              loading: false,
              error:
                err?.message ?? "Couldn't check delivery for this pincode.",
            });
          }
        });
    }, DEBOUNCE_MS);

    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [productId, pincode]);

  return state;
}
