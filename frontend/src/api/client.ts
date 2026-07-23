import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  saveTokens,
} from "../lib/token";

const BASE_URL = "/api";

export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

let onUnauthorized: (() => void) | null = null;
let refreshInFlight: Promise<boolean> | null = null;

export function setUnauthorizedHandler(handler: (() => void) | null): void {
  onUnauthorized = handler;
}

function send(path: string, init: RequestInit): Promise<Response> {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");

  const token = getAccessToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  return fetch(`${BASE_URL}${path}`, { ...init, headers });
}

async function requestNewTokens(): Promise<boolean> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    return false;
  }

  const response = await fetch(`${BASE_URL}/tokens/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!response.ok) {
    clearTokens();
    onUnauthorized?.();
    return false;
  }

  const tokens = await response.json();
  saveTokens(tokens.access_token, tokens.refresh_token);
  return true;
}

function refreshTokens(): Promise<boolean> {
  if (!refreshInFlight) {
    refreshInFlight = requestNewTokens().finally(() => {
      refreshInFlight = null;
    });
  }
  return refreshInFlight;
}

function isRefreshable(path: string): boolean {
  return (
    getRefreshToken() !== null &&
    !path.startsWith("/auth/") &&
    path !== "/tokens/refresh"
  );
}

export async function request<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  let response = await send(path, init);

  if (response.status === 401 && isRefreshable(path)) {
    const refreshed = await refreshTokens();
    if (refreshed) {
      response = await send(path, init);
    }
  }

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const message =
      body && typeof body.message === "string"
        ? body.message
        : `Ошибка запроса: ${response.status}`;
    throw new ApiError(response.status, message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}
