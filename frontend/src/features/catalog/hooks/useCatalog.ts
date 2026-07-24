import { useCallback, useEffect, useState } from "react";
import {
  fetchCategories,
  fetchCategory,
  fetchProducts,
  type ProductQuery,
} from "../../../api/catalog";
import type { Category, Product } from "../../../types/catalog";
import { useAuth } from "../../auth/AuthContext";

type AsyncState<T> = {
  data: T;
  loading: boolean;
  error: string | null;
};

type Reloadable = { reload: () => void };
type ProductsState = AsyncState<Product[]> & { total: number } & Reloadable;

export function useProducts(query: ProductQuery = {}): ProductsState {
  const { isAuthenticated } = useAuth();
  const { page, limit, search, categoryId } = query;
  const [reloadToken, setReloadToken] = useState(0);
  const [state, setState] = useState<AsyncState<Product[]> & { total: number }>({
    data: [],
    total: 0,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    setState((prev) => ({ ...prev, loading: true, error: null }));

    fetchProducts({ page, limit, search, categoryId })
      .then((result) => {
        if (!cancelled) {
          setState({
            data: result.items,
            total: result.total,
            loading: false,
            error: null,
          });
        }
      })
      .catch((error: Error) => {
        if (!cancelled) {
          setState({
            data: [],
            total: 0,
            loading: false,
            error: error.message,
          });
        }
      });

    return () => {
      cancelled = true;
    };
  }, [isAuthenticated, page, limit, search, categoryId, reloadToken]);

  const reload = useCallback(() => setReloadToken((token) => token + 1), []);

  return { ...state, reload };
}

export function useCategories(): AsyncState<Category[]> & Reloadable {
  const { isAuthenticated } = useAuth();
  const [reloadToken, setReloadToken] = useState(0);
  const [state, setState] = useState<AsyncState<Category[]>>({
    data: [],
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    setState((prev) => ({ ...prev, loading: true, error: null }));

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
  }, [isAuthenticated, reloadToken]);

  const reload = useCallback(() => setReloadToken((token) => token + 1), []);

  return { ...state, reload };
}

export function useCategory(categoryId: string | null): Category | null {
  const [category, setCategory] = useState<Category | null>(null);

  useEffect(() => {
    let cancelled = false;
    if (!categoryId) {
      setCategory(null);
      return;
    }

    fetchCategory(categoryId)
      .then((item) => {
        if (!cancelled) {
          setCategory(item);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setCategory(null);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [categoryId]);

  return category;
}
