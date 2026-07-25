import type { ButtonHTMLAttributes, ReactNode } from "react";
import styles from "./Button.module.css";

type Variant = "pink" | "outline" | "dark";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  variant?: Variant;
};

export function Button({ children, variant = "pink", ...rest }: Props) {
  return (
    <button {...rest} className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}
