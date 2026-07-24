import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import { fetchUsdRate } from "../../api/catalog";
import { USD_RATE_CACHE_KEY } from "../../lib/constants";
import { useAuth } from "../auth/AuthContext";

type CurrencyValue = {
  rate: number | null;
  rateDate: string | null;
  ready: boolean;
  toUsd: (priceByn: number) => number | null;
};

type CachedRate = {
  rate: number;
  rateDate: string;
  day: string;
};

const CurrencyContext = createContext<CurrencyValue | null>(null);

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

function readCache(): CachedRate | null {
  try {
    const raw = localStorage.getItem(USD_RATE_CACHE_KEY);
    if (!raw) {
      return null;
    }
    const parsed = JSON.parse(raw) as CachedRate;
    return parsed.day === today() ? parsed : null;
  } catch {
    return null;
  }
}

export function CurrencyProvider({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth();
  const [cache, setCache] = useState<CachedRate | null>(() => readCache());

  useEffect(() => {
    if (!isAuthenticated || cache) {
      return;
    }
    let cancelled = false;
    fetchUsdRate()
      .then(({ rate, date }) => {
        if (cancelled) {
          return;
        }
        const fresh: CachedRate = { rate, rateDate: date, day: today() };
        setCache(fresh);
        localStorage.setItem(USD_RATE_CACHE_KEY, JSON.stringify(fresh));
      })
      .catch(() => {
        // Курс — вспомогательная информация: молча живём без него.
      });
    return () => {
      cancelled = true;
    };
  }, [isAuthenticated, cache]);

  const value = useMemo<CurrencyValue>(() => {
    const rate = cache?.rate ?? null;
    return {
      rate,
      rateDate: cache?.rateDate ?? null,
      ready: rate !== null,
      toUsd: (priceByn: number) =>
        rate && rate > 0 ? Math.round((priceByn / rate) * 100) / 100 : null,
    };
  }, [cache]);

  return (
    <CurrencyContext.Provider value={value}>
      {children}
    </CurrencyContext.Provider>
  );
}

export function useCurrency(): CurrencyValue {
  const value = useContext(CurrencyContext);
  if (!value) {
    throw new Error("useCurrency должен использоваться внутри CurrencyProvider");
  }
  return value;
}
