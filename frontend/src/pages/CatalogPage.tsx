import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { PageTitle } from "../components/ui/PageTitle";
import { SearchBar } from "../components/ui/SearchBar";
import { StateMessage } from "../components/ui/StateMessage";
import { useToast } from "../components/ui/Toast";
import { Hero } from "../features/catalog/components/Hero";
import { ProductForm } from "../features/catalog/components/ProductForm";
import { ProductGrid } from "../features/catalog/components/ProductGrid";
import { useCategories, useProducts } from "../features/catalog/hooks/useCatalog";
import { useAuth } from "../features/auth/AuthContext";
import { deleteProduct } from "../api/catalog";
import { useDebouncedValue } from "../lib/useDebouncedValue";
import type { Product } from "../types/catalog";
import styles from "./CatalogPage.module.css";

type FormState = { product?: Product } | null;

export function CatalogPage() {
  const { isAuthenticated, canEditProducts, canDeleteProducts } = useAuth();
  const { notify } = useToast();
  const [params, setParams] = useSearchParams();
  const categoryId = params.get("category");
  const urlSearch = params.get("search") ?? "";

  const [term, setTerm] = useState(urlSearch);
  const debounced = useDebouncedValue(term, 350);
  const [form, setForm] = useState<FormState>(null);

  useEffect(() => {
    setParams(
      (prev) => {
        const next = new URLSearchParams(prev);
        if (debounced) {
          next.set("search", debounced);
        } else {
          next.delete("search");
        }
        return next;
      },
      { replace: true },
    );
  }, [debounced, setParams]);

  useEffect(() => {
    if (categoryId) {
      document
        .getElementById("products")
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [categoryId]);

  const { data: categories } = useCategories();
  const {
    data: products,
    total,
    loading,
    error,
    reload,
  } = useProducts({
    search: urlSearch || undefined,
    categoryId: categoryId || undefined,
  });

  const handleCategoryChange = (value: string) => {
    setParams((prev) => {
      const next = new URLSearchParams(prev);
      if (value) {
        next.set("category", value);
      } else {
        next.delete("category");
      }
      return next;
    });
  };

  const handleDelete = async (product: Product) => {
    if (!window.confirm(`Удалить продукт «${product.name}»?`)) {
      return;
    }
    try {
      await deleteProduct(product.id);
      reload();
    } catch (cause) {
      notify((cause as Error).message);
    }
  };

  const hasFilters = Boolean(urlSearch || categoryId);

  return (
    <div className={styles.page}>
      <Hero />

      <section id="products" className={styles.section}>
        <div className={styles.head}>
          <PageTitle>Продукты</PageTitle>
          <Link to="/categories" className={styles.allLink}>
            Смотреть категории →
          </Link>
        </div>

        <div className={styles.toolbar}>
          <SearchBar value={term} onChange={setTerm} />
          <select
            className={styles.categorySelect}
            value={categoryId ?? ""}
            onChange={(event) => handleCategoryChange(event.target.value)}
          >
            <option value="">Все категории</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
          {!loading && !error && hasFilters && (
            <span className={styles.count}>Найдено: {total}</span>
          )}
          {canEditProducts && categories.length > 0 && (
            <div className={styles.spacer}>
              <Button variant="pink" onClick={() => setForm({})}>
                + Добавить продукт
              </Button>
            </div>
          )}
        </div>

        {loading && products.length === 0 && !error && (
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
            title={hasFilters ? "Ничего не найдено" : "Пока пусто"}
            text={
              hasFilters
                ? "Попробуйте изменить запрос или сбросить фильтр."
                : "В каталоге ещё нет продуктов."
            }
          />
        )}

        {!error && products.length > 0 && (
          <ProductGrid
            products={products}
            onEdit={canEditProducts ? (product) => setForm({ product }) : undefined}
            onDelete={canDeleteProducts ? handleDelete : undefined}
          />
        )}
      </section>

      {form && (
        <ProductForm
          product={form.product}
          categories={categories}
          onClose={() => setForm(null)}
          onSaved={reload}
        />
      )}
    </div>
  );
}
