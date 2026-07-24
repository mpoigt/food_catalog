export type Role = "user" | "advanced" | "admin";

export type CurrentUser = {
  id: string;
  username: string;
  email: string;
  role: Role;
};
