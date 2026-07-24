import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import { fetchMe, login as loginRequest } from "../../api/auth";
import { setUnauthorizedHandler } from "../../api/client";
import { clearTokens, getAccessToken, saveTokens } from "../../lib/token";
import type { CurrentUser, Role } from "../../types/auth";

type AuthValue = {
  isAuthenticated: boolean;
  user: CurrentUser | null;
  role: Role | null;
  canEditProducts: boolean;
  canEditSpecialNote: boolean;
  canDeleteProducts: boolean;
  canManageCategories: boolean;
  isAdmin: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
};

const AuthContext = createContext<AuthValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => getAccessToken());
  const [user, setUser] = useState<CurrentUser | null>(null);

  const loadMe = useCallback(async () => {
    try {
      setUser(await fetchMe());
    } catch {
      setUser(null);
    }
  }, []);

  const signIn = useCallback(
    async (email: string, password: string) => {
      const tokens = await loginRequest(email, password);
      saveTokens(tokens.access_token, tokens.refresh_token);
      setToken(tokens.access_token);
      await loadMe();
    },
    [loadMe],
  );

  const signOut = useCallback(() => {
    clearTokens();
    setToken(null);
    setUser(null);
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(() => {
      setToken(null);
      setUser(null);
    });
    return () => setUnauthorizedHandler(null);
  }, []);

  useEffect(() => {
    if (token && !user) {
      void loadMe();
    }
  }, [token, user, loadMe]);

  const value = useMemo<AuthValue>(() => {
    const role = user?.role ?? null;
    const isPrivileged = role === "advanced" || role === "admin";
    return {
      isAuthenticated: token !== null,
      user,
      role,
      canEditProducts: role !== null,
      canEditSpecialNote: isPrivileged,
      canDeleteProducts: isPrivileged,
      canManageCategories: isPrivileged,
      isAdmin: role === "admin",
      signIn,
      signOut,
    };
  }, [token, user, signIn, signOut]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthValue {
  const value = useContext(AuthContext);
  if (!value) {
    throw new Error("useAuth должен использоваться внутри AuthProvider");
  }
  return value;
}
