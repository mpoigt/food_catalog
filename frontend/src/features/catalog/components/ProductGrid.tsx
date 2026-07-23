import type { Product } from "../../../types/catalog";
import { ProductCard } from "./ProductCard";
import styles from "./ProductGrid.module.css";

type Props = {
  products: Product[];
};

export function ProductGrid({ products }: Props) {
  return (
    <div className={styles.grid}>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
