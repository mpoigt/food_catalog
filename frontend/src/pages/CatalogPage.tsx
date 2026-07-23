import { Link } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Chip } from "../components/ui/Chip";
import { StateMessage } from "../components/ui/StateMessage";
import { Hero } from "../features/catalog/components/Hero";
import { ProductGrid } from "../features/catalog/components/ProductGrid";
import { useProducts } from "../features/catalog/hooks/useCatalog";
import { useAuth } from "../features/auth/AuthContext";
import styles from "./CatalogPage.module.css";

export function CatalogPage() {
  const { isAuthenticated } = useAuth();
  const { data: products, loading, error } = useProducts();

  return (
    <div className={styles.page}>
      <Hero />

      <section className={styles.section}>
        <div className={styles.head}>
          <Chip tone="dark">Продукты</Chip>
          <Link to="/categories" className={styles.allLink}>
            Смотреть категории →
          </Link>
        </div>

        {loading && (
          <StateMessage icon="⏳" title="Загружаем продукты…" />
        )}

        {!loading && error && !isAuthenticated && (
          <StateMessage
            icon="🔒"
            title="Нужно войти"
            text="Каталог доступен авторизованным пользователям."
            action={
              <Link to="/login">
                <Button variant="pink">Войти</Button>
              </Link>
            }
          />
        )}

        {!loading && error && isAuthenticated && (
          <StateMessage icon="⚠️" title="Не удалось загрузить" text={error} />
        )}

        {!loading && !error && products.length === 0 && (
          <StateMessage
            icon="🧺"
            title="Пока пусто"
            text="В каталоге ещё нет продуктов."
          />
        )}

        {!loading && !error && products.length > 0 && (
          <ProductGrid products={products} />
        )}
      </section>
    </div>
  );
}
