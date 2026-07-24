import { request } from "./client";
import type { Role } from "../types/auth";

export type AdminUser = {
  id: string;
  username: string;
  email: string;
  role: Role;
  isBlocked: boolean;
};

type AdminUserDto = {
  id: string;
  username: string;
  email: string;
  role: Role;
  is_blocked: boolean;
};

type PaginatedUsersDto = {
  total: number;
  page: number;
  limit: number;
  items: AdminUserDto[];
};

function toUser(dto: AdminUserDto): AdminUser {
  return {
    id: dto.id,
    username: dto.username,
    email: dto.email,
    role: dto.role,
    isBlocked: dto.is_blocked,
  };
}

export async function fetchUsers(): Promise<AdminUser[]> {
  const data = await request<PaginatedUsersDto>("/users/?limit=100");
  return data.items.map(toUser);
}

export type CreateUserInput = {
  username: string;
  email: string;
  password: string;
  role: Role;
};

export async function createUser(input: CreateUserInput): Promise<AdminUser> {
  const dto = await request<AdminUserDto>("/users/", {
    method: "POST",
    body: JSON.stringify(input),
  });
  return toUser(dto);
}

export type UpdateUserInput = Partial<{
  username: string;
  email: string;
  role: Role;
  is_blocked: boolean;
  password: string;
}>;

export async function updateUser(
  id: string,
  patch: UpdateUserInput,
): Promise<AdminUser> {
  const dto = await request<AdminUserDto>(`/users/${id}`, {
    method: "PATCH",
    body: JSON.stringify(patch),
  });
  return toUser(dto);
}

export async function deleteUser(id: string): Promise<void> {
  await request(`/users/${id}`, { method: "DELETE" });
}
