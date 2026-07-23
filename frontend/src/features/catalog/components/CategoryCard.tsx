import { CATEGORY_ICON } from "../../../lib/constants";
import type { Category } from "../../../types/catalog";
import styles from "./CategoryCard.module.css";

type Props = {
  category: Category;
};

export function CategoryCard({ category }: Props) {
  return (
    <article className={styles.card}>
      <div className={styles.icon}>
        {CATEGORY_ICON[category.name] ?? "🍽️"}
      </div>
      <h3 className={styles.name}>{category.name}</h3>
    </article>
  );
}
