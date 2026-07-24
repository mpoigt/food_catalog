import type { ReactNode } from "react";
import styles from "./Chip.module.css";

type Tone = "dark" | "pink" | "yellow";

type Props = {
  children: ReactNode;
  tone?: Tone;
  className?: string;
};

export function Chip({ children, tone = "dark", className }: Props) {
  return (
    <span className={`${styles.chip} ${styles[tone]} ${className ?? ""}`}>
      {children}
    </span>
  );
}
