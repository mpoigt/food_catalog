import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import { login as loginRequest } from "../../api/auth";
import { setUnauthorizedHandler } from "../../api/client";
import { clearTokens, getAccessToken, saveTokens } from "../../lib/token";

type AuthValue = {
  isAuthenticated: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
};

const AuthContext = createContext<AuthValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => getAccessToken());

  const signIn = useCallback(async (email: string, password: string) => {
    const tokens = await loginRequest(email, password);
    saveTokens(tokens.access_token, tokens.refresh_token);
    setToken(tokens.access_token);
  }, []);

  const signOut = useCallback(() => {
    clearTokens();
    setToken(null);
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(() => setToken(null));
    return () => setUnauthorizedHandler(null);
  }, []);

  const value = useMemo(
    () => ({ isAuthenticated: token !== null, signIn, signOut }),
    [token, signIn, signOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthValue {
  const value = useContext(AuthContext);
  if (!value) {
    throw new Error("useAuth должен использоваться внутри AuthProvider");
  }
  return value;
}
