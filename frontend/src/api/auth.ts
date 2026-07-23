import { request } from "./client";

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
