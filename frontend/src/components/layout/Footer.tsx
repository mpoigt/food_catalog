import styles from "./Footer.module.css";

export function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <p className={styles.text}>
          Каталог продуктов <span className={styles.heart}>♥</span> свежесть
          каждый день
        </p>
      </div>
    </footer>
  );
}
