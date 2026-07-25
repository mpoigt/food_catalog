import { request } from "./client";
import type { CurrentUser } from "../types/auth";

type TokenPairDto = {
  access_token: string;
  refresh_token: string;
};

export async function login(
  email: string,
  password: string,
): Promise<TokenPairDto> {
  return request<TokenPairDto>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function register(
  username: string,
  email: string,
  password: string,
): Promise<void> {
  await request("/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  });
}

export async function fetchMe(): Promise<CurrentUser> {
  return request<CurrentUser>("/auth/me");
}
