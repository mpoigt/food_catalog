import type { ReactNode } from "react";
import styles from "./Chip.module.css";

type Tone = "dark" | "pink" | "yellow";

type Props = {
  children: ReactNode;
  tone?: Tone;
};

export function Chip({ children, tone = "dark" }: Props) {
  return <span className={`${styles.chip} ${styles[tone]}`}>{children}</span>;
}
