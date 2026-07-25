import { useState } from "react";
import type { FormEvent } from "react";
import { Button } from "../../components/ui/Button";
import { Field, FormError, Input, Select } from "../../components/ui/Field";
import { Modal } from "../../components/ui/Modal";
import { createUser } from "../../api/users";
import { ROLES, ROLE_LABELS } from "../../lib/constants";
import type { Role } from "../../types/auth";
import styles from "../catalog/components/ProductForm.module.css";

type Props = {
  onClose: () => void;
  onSaved: () => void;
};

export function UserForm({ onClose, onSaved }: Props) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<Role>("user");
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setPending(true);
    setError(null);
    try {
      await createUser({ username, email, password, role });
      onSaved();
      onClose();
    } catch (cause) {
      setError((cause as Error).message);
    } finally {
      setPending(false);
    }
  };

  return (
    <Modal title="Новый пользователь" onClose={onClose}>
      <form onSubmit={handleSubmit}>
        {error && <FormError message={error} />}
        <Field label="Имя пользователя">
          <Input
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            required
            minLength={3}
            maxLength={50}
          />
        </Field>
        <Field label="Почта">
          <Input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </Field>
        <Field label="Пароль">
          <Input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            minLength={8}
          />
        </Field>
        <Field label="Роль">
          <Select
            value={role}
            onChange={(event) => setRole(event.target.value as Role)}
          >
            {ROLES.map((value) => (
              <option key={value} value={value}>
                {ROLE_LABELS[value]}
              </option>
            ))}
          </Select>
        </Field>
        <div className={styles.actions}>
          <Button variant="outline" type="button" onClick={onClose}>
            Отмена
          </Button>
          <Button variant="pink" type="submit" disabled={pending}>
            {pending ? "Создаём…" : "Создать"}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
