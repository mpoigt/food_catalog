import { useRef, useState } from "react";
import { fetchProductPriceUsd } from "../../../api/catalog";
import { RATE_HOVER_DELAY_MS } from "../../../lib/constants";

export function useUsdPrice(productId: string) {
  const [usd, setUsd] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const timer = useRef<number | null>(null);

  const start = () => {
    if (usd !== null || loading) {
      return;
    }
    timer.current = window.setTimeout(() => {
      setLoading(true);
      setFailed(false);
      fetchProductPriceUsd(productId)
        .then(setUsd)
        .catch(() => setFailed(true))
        .finally(() => setLoading(false));
    }, RATE_HOVER_DELAY_MS);
  };

  const cancel = () => {
    if (timer.current !== null) {
      window.clearTimeout(timer.current);
      timer.current = null;
    }
  };

  return { usd, loading, failed, start, cancel };
}
