import type { ReactNode } from "react";
import styles from "./PageTitle.module.css";

export function PageTitle({ children }: { children: ReactNode }) {
  return <span className={styles.title}>{children}</span>;
}
