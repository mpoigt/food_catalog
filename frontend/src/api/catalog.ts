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
  category_name: string;
  description: string;
  price: string;
  note_common: string | null;
  note_special: string | null;
  image_url: string | null;
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

function toProduct(dto: ProductDto): Product {
  return {
    id: dto.id,
    name: dto.name,
    categoryId: dto.category_id,
    categoryName: dto.category_name,
    description: dto.description,
    price: Number(dto.price),
    noteCommon: dto.note_common,
    noteSpecial: dto.note_special,
    image: dto.image_url ?? undefined,
  };
}

export async function fetchCategories(): Promise<Category[]> {
  const data = await request<CategoryDto[]>("/categories/");
  return data.map(toCategory);
}

export async function fetchCategory(categoryId: string): Promise<Category> {
  const data = await request<CategoryDto>(`/categories/${categoryId}`);
  return toCategory(data);
}

export async function fetchProducts(
  query: ProductQuery = {},
): Promise<{ items: Product[]; total: number }> {
  const params = new URLSearchParams();
  if (query.page) params.set("page", String(query.page));
  if (query.limit) params.set("limit", String(query.limit));
  if (query.search) params.set("search", query.search);
  if (query.categoryId) params.set("category_id", query.categoryId);

  const data = await request<PaginatedProductsDto>(`/products/?${params}`);
  return { items: data.items.map(toProduct), total: data.total };
}

export type UsdRate = {
  rate: number;
  date: string;
};

export async function fetchUsdRate(): Promise<UsdRate> {
  const data = await request<{ rate: string; date: string }>(
    "/currency/usd-rate",
  );
  return { rate: Number(data.rate), date: data.date };
}

export type ProductInput = {
  name: string;
  categoryId: string;
  description: string;
  price: number;
  noteCommon: string | null;
  noteSpecial: string | null;
};

function toProductBody(input: ProductInput) {
  return {
    name: input.name,
    category_id: input.categoryId,
    description: input.description,
    price: input.price,
    note_common: input.noteCommon || null,
    note_special: input.noteSpecial || null,
  };
}

export async function createProduct(input: ProductInput): Promise<Product> {
  const dto = await request<ProductDto>("/products/", {
    method: "POST",
    body: JSON.stringify(toProductBody(input)),
  });
  return toProduct(dto);
}

export async function updateProduct(
  id: string,
  input: ProductInput,
): Promise<Product> {
  const dto = await request<ProductDto>(`/products/${id}`, {
    method: "PATCH",
    body: JSON.stringify(toProductBody(input)),
  });
  return toProduct(dto);
}

export async function deleteProduct(id: string): Promise<void> {
  await request(`/products/${id}`, { method: "DELETE" });
}

export async function uploadProductImage(
  id: string,
  file: File,
): Promise<Product> {
  const form = new FormData();
  form.append("file", file);
  const dto = await request<ProductDto>(`/products/${id}/image`, {
    method: "POST",
    body: form,
  });
  return toProduct(dto);
}

export async function createCategory(name: string): Promise<Category> {
  const dto = await request<CategoryDto>("/categories/", {
    method: "POST",
    body: JSON.stringify({ name }),
  });
  return toCategory(dto);
}

export async function updateCategory(
  id: string,
  name: string,
): Promise<Category> {
  const dto = await request<CategoryDto>(`/categories/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ name }),
  });
  return toCategory(dto);
}

export async function deleteCategory(id: string): Promise<void> {
  await request(`/categories/${id}`, { method: "DELETE" });
}
