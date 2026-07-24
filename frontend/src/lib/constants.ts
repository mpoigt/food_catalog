export const BRAND = "Каталог";

export const CURRENCY = "р";

export const CATEGORY_ICON: Record<string, string> = {
  Еда: "🥖",
  Вкусности: "🍯",
  Вода: "🥤",
};

export const NAV_LINKS = [
  { label: "Продукты", to: "/" },
  { label: "Категории", to: "/categories" },
  { label: "О нас", to: "/about" },
];

export const ROLES = ["user", "advanced", "admin"] as const;

export const ROLE_LABELS: Record<string, string> = {
  user: "Простой",
  advanced: "Продвинутый",
  admin: "Администратор",
};

export const ACCESS_TOKEN_KEY = "access_token";

export const REFRESH_TOKEN_KEY = "refresh_token";

export const USD_RATE_CACHE_KEY = "usd_rate";
