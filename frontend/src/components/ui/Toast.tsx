import { createContext, useCallback, useContext, useState } from "react";
import type { ReactNode } from "react";
import styles from "./Toast.module.css";

type ToastKind = "error" | "success";

type ToastItem = {
  id: number;
  message: string;
  kind: ToastKind;
};

type ToastValue = {
  notify: (message: string, kind?: ToastKind) => void;
};

const ToastContext = createContext<ToastValue | null>(null);
const AUTO_DISMISS_MS = 4000;

let nextId = 0;

export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([]);

  const dismiss = useCallback((id: number) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  }, []);

  const notify = useCallback(
    (message: string, kind: ToastKind = "error") => {
      const id = nextId++;
      setItems((prev) => [...prev, { id, message, kind }]);
      window.setTimeout(() => dismiss(id), AUTO_DISMISS_MS);
    },
    [dismiss],
  );

  return (
    <ToastContext.Provider value={{ notify }}>
      {children}
      <div className={styles.stack}>
        {items.map((item) => (
          <button
            key={item.id}
            type="button"
            className={`${styles.toast} ${styles[item.kind]}`}
            onClick={() => dismiss(item.id)}
          >
            {item.message}
          </button>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastValue {
  const value = useContext(ToastContext);
  if (!value) {
    throw new Error("useToast должен использоваться внутри ToastProvider");
  }
  return value;
}
