import { Link, NavLink } from "react-router-dom";
import { NAV_LINKS } from "../../lib/constants";
import { useAuth } from "../../features/auth/AuthContext";
import { Button } from "../ui/Button";
import styles from "./Header.module.css";

export function Header() {
  const { isAuthenticated, isAdmin, signOut } = useAuth();

  const links = isAdmin
    ? [...NAV_LINKS, { label: "Пользователи", to: "/users" }]
    : NAV_LINKS;

  return (
    <header className={styles.header}>
      <Link to="/" className={styles.logo}>
        каталог
        <span className={styles.logoAccent}>продуктов</span>
      </Link>

      <nav className={styles.nav}>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            className={({ isActive }) =>
              isActive ? `${styles.link} ${styles.active}` : styles.link
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>

      <div className={styles.actions}>
        {isAuthenticated ? (
          <>
            <Link to="/profile" className={styles.avatar} aria-label="Профиль">
              👤
            </Link>
            <Button variant="outline" onClick={signOut}>
              Выйти
            </Button>
          </>
        ) : (
          <Link to="/login">
            <Button variant="pink">Войти</Button>
          </Link>
        )}
      </div>
    </header>
  );
}
