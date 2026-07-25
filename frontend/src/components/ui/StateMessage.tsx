import type { ReactNode } from "react";
import styles from "./StateMessage.module.css";

type Props = {
  icon: string;
  title: string;
  text?: string;
  action?: ReactNode;
};

export function StateMessage({ icon, title, text, action }: Props) {
  return (
    <div className={styles.wrap}>
      <span className={styles.icon}>{icon}</span>
      <h3 className={styles.title}>{title}</h3>
      {text && <p className={styles.text}>{text}</p>}
      {action && <div className={styles.action}>{action}</div>}
    </div>
  );
}
