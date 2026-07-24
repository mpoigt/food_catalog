import { useCallback, useEffect, useState } from "react";
import { fetchUsers, type AdminUser } from "../../api/users";

type UsersState = {
  data: AdminUser[];
  loading: boolean;
  error: string | null;
  reload: () => void;
};

export function useUsers(enabled: boolean): UsersState {
  const [reloadToken, setReloadToken] = useState(0);
  const [state, setState] = useState<Omit<UsersState, "reload">>({
    data: [],
    loading: true,
    error: null,
  });

  useEffect(() => {
    if (!enabled) {
      setState({ data: [], loading: false, error: null });
      return;
    }
    let cancelled = false;
    setState((prev) => ({ ...prev, loading: true, error: null }));

    fetchUsers()
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
  }, [enabled, reloadToken]);

  const reload = useCallback(() => setReloadToken((token) => token + 1), []);

  return { ...state, reload };
}
