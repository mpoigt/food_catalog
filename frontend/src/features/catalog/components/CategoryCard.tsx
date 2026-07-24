import { Link } from "react-router-dom";
import type { Category } from "../../../types/catalog";
import styles from "./CategoryCard.module.css";

type Props = {
  category: Category;
  onEdit?: (category: Category) => void;
  onDelete?: (category: Category) => void;
};

export function CategoryCard({ category, onEdit, onDelete }: Props) {
  return (
    <Link to={`/?category=${category.id}`} className={styles.card}>
      <span className={styles.icon}>
        <img className={styles.iconImg} src="/candy.png" alt="" />
      </span>
      <h3 className={styles.name}>{category.name}</h3>
      <span className={styles.cta}>Смотреть продукты →</span>
      {(onEdit || onDelete) && (
        <div className={styles.actions}>
          {onEdit && (
            <button
              type="button"
              className={styles.action}
              aria-label="Изменить"
              onClick={(event) => {
                event.preventDefault();
                onEdit(category);
              }}
            >
              ✎
            </button>
          )}
          {onDelete && (
            <button
              type="button"
              className={`${styles.action} ${styles.danger}`}
              aria-label="Удалить"
              onClick={(event) => {
                event.preventDefault();
                onDelete(category);
              }}
            >
              🗑
            </button>
          )}
        </div>
      )}
    </Link>
  );
}
