import { CATEGORY_ICON } from "../../../lib/constants";
import type { Product } from "../../../types/catalog";
import { PriceTag } from "./PriceTag";
import styles from "./ProductCard.module.css";

type Props = {
  product: Product;
  onEdit?: (product: Product) => void;
  onDelete?: (product: Product) => void;
};

export function ProductCard({ product, onEdit, onDelete }: Props) {
  const showActions = Boolean(onEdit || onDelete);

  return (
    <article className={styles.card}>
      <div className={styles.thumb}>
        {product.image ? (
          <img className={styles.image} src={product.image} alt={product.name} />
        ) : (
          <span className={styles.emoji}>
            {CATEGORY_ICON[product.categoryName] ?? "🍽️"}
          </span>
        )}
        {product.noteCommon && (
          <span className={styles.sticker}>{product.noteCommon}</span>
        )}
        {showActions && (
          <div className={styles.actions}>
            {onEdit && (
              <button
                type="button"
                className={styles.action}
                aria-label="Изменить"
                onClick={() => onEdit(product)}
              >
                ✎
              </button>
            )}
            {onDelete && (
              <button
                type="button"
                className={`${styles.action} ${styles.danger}`}
                aria-label="Удалить"
                onClick={() => onDelete(product)}
              >
                🗑
              </button>
            )}
          </div>
        )}
      </div>

      <div className={styles.body}>
        <span className={styles.category}>{product.categoryName}</span>
        <h3 className={styles.name}>{product.name}</h3>
        <p className={styles.description}>{product.description}</p>

        {product.noteSpecial && (
          <p className={styles.special}>{product.noteSpecial}</p>
        )}

        <div className={styles.footer}>
          <PriceTag price={product.price} />
        </div>
      </div>
    </article>
  );
}
