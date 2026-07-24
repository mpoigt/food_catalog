import { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Chip } from "../components/ui/Chip";
import { PageTitle } from "../components/ui/PageTitle";
import { StateMessage } from "../components/ui/StateMessage";
import { useAuth } from "../features/auth/AuthContext";
import { ROLE_LABELS } from "../lib/constants";
import styles from "./ProfilePage.module.css";

export function ProfilePage() {
  const { isAuthenticated, user } = useAuth();
  const [hasIcon, setHasIcon] = useState(true);

  if (!isAuthenticated || !user) {
    return (
      <section className={styles.section}>
        <StateMessage
          icon="🔒"
          title="Нужно войти"
          text="Профиль доступен авторизованным пользователям."
          action={
            <Link to="/login">
              <Button variant="pink">Войти</Button>
            </Link>
          }
        />
      </section>
    );
  }

  return (
    <section className={styles.section}>
      <PageTitle>Профиль</PageTitle>

      <div className={styles.card}>
        <div className={styles.avatar}>
          {hasIcon ? (
            <img
              className={styles.photo}
              src="/person_icon.jpg"
              alt="Фото профиля"
              onError={() => setHasIcon(false)}
            />
          ) : (
            <span className={styles.fallback}>👤</span>
          )}
        </div>

        <div className={styles.info}>
          <h1 className={styles.name}>{user.username}</h1>
          <Chip tone="pink">{ROLE_LABELS[user.role] ?? user.role}</Chip>

          <dl className={styles.fields}>
            <div className={styles.row}>
              <dt className={styles.term}>Почта</dt>
              <dd className={styles.value}>{user.email}</dd>
            </div>
            <div className={styles.row}>
              <dt className={styles.term}>Роль</dt>
              <dd className={styles.value}>
                {ROLE_LABELS[user.role] ?? user.role}
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </section>
  );
}
