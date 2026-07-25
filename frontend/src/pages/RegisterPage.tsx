import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Chip } from "../components/ui/Chip";
import { register } from "../api/auth";
import { useAuth } from "../features/auth/AuthContext";
import styles from "./LoginPage.module.css";

export function RegisterPage() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setPending(true);
    setError(null);
    try {
      await register(username, email, password);
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
        <Chip tone="pink">Регистрация ♥</Chip>
        <h1 className={styles.title}>Создать аккаунт</h1>
        <p className={styles.subtitle}>
          Зарегистрируйтесь, чтобы открыть каталог продуктов.
        </p>

        <label className={styles.field}>
          <span className={styles.label}>Имя пользователя</span>
          <input
            className={styles.input}
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            placeholder="username"
            minLength={3}
            maxLength={50}
            required
          />
        </label>

        <label className={styles.field}>
          <span className={styles.label}>Почта</span>
          <input
            className={styles.input}
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
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
            placeholder="минимум 8 символов"
            minLength={8}
            required
          />
        </label>

        {error && <p className={styles.error}>{error}</p>}

        <Button variant="pink" type="submit" disabled={pending}>
          {pending ? "Создаём…" : "Зарегистрироваться"}
        </Button>

        <p className={styles.foot}>
          Уже есть аккаунт? <Link to="/login">Войти</Link>
        </p>
      </form>
    </section>
  );
}
