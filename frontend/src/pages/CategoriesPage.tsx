import { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { PageTitle } from "../components/ui/PageTitle";
import { StateMessage } from "../components/ui/StateMessage";
import { useToast } from "../components/ui/Toast";
import { CategoryCard } from "../features/catalog/components/CategoryCard";
import { CategoryForm } from "../features/catalog/components/CategoryForm";
import { useCategories } from "../features/catalog/hooks/useCatalog";
import { useAuth } from "../features/auth/AuthContext";
import { deleteCategory } from "../api/catalog";
import type { Category } from "../types/catalog";
import styles from "./CategoriesPage.module.css";

type FormState = { category?: Category } | null;

export function CategoriesPage() {
  const { isAuthenticated, canManageCategories } = useAuth();
  const { notify } = useToast();
  const { data: categories, loading, error, reload } = useCategories();
  const [form, setForm] = useState<FormState>(null);

  const handleDelete = async (category: Category) => {
    if (
      !window.confirm(
        `Удалить категорию «${category.name}»? Все её продукты также будут удалены.`,
      )
    ) {
      return;
    }
    try {
      await deleteCategory(category.id);
      reload();
    } catch (cause) {
      notify((cause as Error).message);
    }
  };

  return (
    <section className={styles.section}>
      <div className={styles.head}>
        <div>
          <PageTitle>Категории</PageTitle>
          <p className={styles.hint}>Справочник категорий каталога</p>
        </div>
        {canManageCategories && (
          <Button variant="pink" onClick={() => setForm({})}>
            + Добавить категорию
          </Button>
        )}
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
        <div className={styles.list}>
          {categories.map((category) => (
            <CategoryCard
              key={category.id}
              category={category}
              onEdit={
                canManageCategories
                  ? (item) => setForm({ category: item })
                  : undefined
              }
              onDelete={canManageCategories ? handleDelete : undefined}
            />
          ))}
        </div>
      )}

      {form && (
        <CategoryForm
          category={form.category}
          onClose={() => setForm(null)}
          onSaved={reload}
        />
      )}
    </section>
  );
}
