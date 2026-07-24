import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Chip } from "../components/ui/Chip";
import { useAuth } from "../features/auth/AuthContext";
import styles from "./LoginPage.module.css";

export function LoginPage() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setPending(true);
    setError(null);
    try {
      await signIn(email, password);
      navigate("/");
    } catch (cause) {
      setError((cause as Error).message);
    } finally {
      setPending(false);
    }
  };

  return (
    <section className={styles.wrap}>
      <form className={styles.card} onSubmit={handleSubmit}>
        <Chip tone="pink">Вход ♥</Chip>
        <h1 className={styles.title}>С возвращением!</h1>
        <p className={styles.subtitle}>
          Войдите, чтобы увидеть каталог продуктов.
        </p>

        <label className={styles.field}>
          <span className={styles.label}>Почта</span>
          <input
            className={styles.input}
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="admin@example.com"
            required
          />
        </label>

        <label className={styles.field}>
          <span className={styles.label}>Пароль</span>
          <input
            className={styles.input}
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="••••••••"
            required
          />
        </label>

        {error && <p className={styles.error}>{error}</p>}

        <Button variant="pink" type="submit" disabled={pending}>
          {pending ? "Входим…" : "Войти"}
        </Button>

        <p className={styles.foot}>
          Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
        </p>
      </form>
    </section>
  );
}
