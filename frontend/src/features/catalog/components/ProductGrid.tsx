import type { Product } from "../../../types/catalog";
import { ProductCard } from "./ProductCard";
import styles from "./ProductGrid.module.css";

type Props = {
  products: Product[];
  onEdit?: (product: Product) => void;
  onDelete?: (product: Product) => void;
};

export function ProductGrid({ products, onEdit, onDelete }: Props) {
  return (
    <div className={styles.grid}>
      {products.map((product) => (
        <ProductCard
          key={product.id}
          product={product}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
