import styles from "./ComingSoonPage.module.css";

type Props = {
  title: string;
};

export function ComingSoonPage({ title }: Props) {
  return (
    <section className={styles.panel}>
      <span className={styles.stars}>★ ★ ★</span>
      <h1 className={styles.title}>{title}</h1>
      <p className={styles.text}>Раздел в разработке</p>
    </section>
  );
}
