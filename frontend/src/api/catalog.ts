import { request } from "./client";
import type { Category, Product } from "../types/catalog";

type CategoryDto = {
  id: string;
  name: string;
};

type ProductDto = {
  id: string;
  name: string;
  category_id: string;
  description: string;
  price: string;
  note_common: string | null;
  note_special: string | null;
};

type PaginatedProductsDto = {
  total: number;
  page: number;
  limit: number;
  items: ProductDto[];
};

export type ProductQuery = {
  page?: number;
  limit?: number;
  search?: string;
  categoryId?: string;
};

function toCategory(dto: CategoryDto): Category {
  return { id: dto.id, name: dto.name };
}

function toProduct(dto: ProductDto, categories: Category[]): Product {
  const category = categories.find((item) => item.id === dto.category_id);
  return {
    id: dto.id,
    name: dto.name,
    categoryId: dto.category_id,
    categoryName: category ? category.name : "",
    description: dto.description,
    price: Number(dto.price),
    noteCommon: dto.note_common,
    noteSpecial: dto.note_special,
  };
}

export async function fetchCategories(): Promise<Category[]> {
  const data = await request<CategoryDto[]>("/categories/");
  return data.map(toCategory);
}

export async function fetchProducts(
  query: ProductQuery = {},
): Promise<{ items: Product[]; total: number }> {
  const categories = await fetchCategories();

  const params = new URLSearchParams();
  if (query.page) params.set("page", String(query.page));
  if (query.limit) params.set("limit", String(query.limit));
  if (query.search) params.set("search", query.search);
  if (query.categoryId) params.set("category_id", query.categoryId);

  const data = await request<PaginatedProductsDto>(`/products/?${params}`);
  return {
    items: data.items.map((item) => toProduct(item, categories)),
    total: data.total,
  };
}

export async function fetchProductPriceUsd(productId: string): Promise<number> {
  const data = await request<{ price_usd: string }>(
    `/products/${productId}/price-usd`,
  );
  return Number(data.price_usd);
}
