import { useCallback, useEffect, useRef, useState } from "react";
import {
  fetchProductPriceUsd,
  type ProductPriceUsd,
} from "../../../api/catalog";

export type PriceUsdState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "ready"; data: ProductPriceUsd }
  | { status: "error" };

export function usePriceUsdOnHover(productId: string, delayMs = 350) {
  const [state, setState] = useState<PriceUsdState>({ status: "idle" });
  const timer = useRef<number | null>(null);
  const cache = useRef<ProductPriceUsd | null>(null);

  const cancel = useCallback(() => {
    if (timer.current !== null) {
      window.clearTimeout(timer.current);
      timer.current = null;
    }
  }, []);

  const start = useCallback(() => {
    if (cache.current) {
      setState({ status: "ready", data: cache.current });
      return;
    }
    if (timer.current !== null) {
      return;
    }
    timer.current = window.setTimeout(() => {
      timer.current = null;
      setState({ status: "loading" });
      fetchProductPriceUsd(productId)
        .then((data) => {
          cache.current = data;
          setState({ status: "ready", data });
        })
        .catch(() => setState({ status: "error" }));
    }, delayMs);
  }, [productId, delayMs]);

  useEffect(() => cancel, [cancel]);

  return { state, start, cancel };
}
