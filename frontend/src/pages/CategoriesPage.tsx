import { Link } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Chip } from "../components/ui/Chip";
import { StateMessage } from "../components/ui/StateMessage";
import { CategoryCard } from "../features/catalog/components/CategoryCard";
import { useCategories } from "../features/catalog/hooks/useCatalog";
import { useAuth } from "../features/auth/AuthContext";
import styles from "./CategoriesPage.module.css";

export function CategoriesPage() {
  const { isAuthenticated } = useAuth();
  const { data: categories, loading, error } = useCategories();

  return (
    <section className={styles.section}>
      <div className={styles.head}>
        <Chip tone="dark">Категории</Chip>
        <p className={styles.hint}>Справочник категорий каталога</p>
      </div>

      {loading && <StateMessage icon="⏳" title="Загружаем категории…" />}

      {!loading && error && !isAuthenticated && (
        <StateMessage
          icon="🔒"
          title="Нужно войти"
          text="Справочник доступен авторизованным пользователям."
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

      {!loading && !error && categories.length === 0 && (
        <StateMessage icon="📁" title="Категорий пока нет" />
      )}

      {!loading && !error && categories.length > 0 && (
        <div className={styles.grid}>
          {categories.map((category) => (
            <CategoryCard key={category.id} category={category} />
          ))}
        </div>
      )}
    </section>
  );
}
