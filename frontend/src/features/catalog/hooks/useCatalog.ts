import { useEffect, useState } from "react";
import { fetchCategories, fetchProducts } from "../../../api/catalog";
import type { Category, Product } from "../../../types/catalog";
import { useAuth } from "../../auth/AuthContext";

type AsyncState<T> = {
  data: T;
  loading: boolean;
  error: string | null;
};

export function useProducts(): AsyncState<Product[]> {
  const { isAuthenticated } = useAuth();
  const [state, setState] = useState<AsyncState<Product[]>>({
    data: [],
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    setState({ data: [], loading: true, error: null });

    fetchProducts()
      .then((result) => {
        if (!cancelled) {
          setState({ data: result.items, loading: false, error: null });
        }
      })
      .catch((error: Error) => {
        if (!cancelled) {
          setState({ data: [], loading: false, error: error.message });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [isAuthenticated]);

  return state;
}

export function useCategories(): AsyncState<Category[]> {
  const { isAuthenticated } = useAuth();
  const [state, setState] = useState<AsyncState<Category[]>>({
    data: [],
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    setState({ data: [], loading: true, error: null });

    fetchCategories()
      .then((items) => {
        if (!cancelled) {
          setState({ data: items, loading: false, error: null });
        }
      })
      .catch((error: Error) => {
        if (!cancelled) {
          setState({ data: [], loading: false, error: error.message });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [isAuthenticated]);

  return state;
}
