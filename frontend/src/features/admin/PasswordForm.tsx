import { useState } from "react";
import type { FormEvent } from "react";
import { Button } from "../../components/ui/Button";
import { Field, FormError, Input } from "../../components/ui/Field";
import { Modal } from "../../components/ui/Modal";
import { updateUser, type AdminUser } from "../../api/users";
import styles from "../catalog/components/ProductForm.module.css";

type Props = {
  user: AdminUser;
  onClose: () => void;
  onSaved: () => void;
};

export function PasswordForm({ user, onClose, onSaved }: Props) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setPending(true);
    setError(null);
    try {
      await updateUser(user.id, { password });
      onSaved();
      onClose();
    } catch (cause) {
      setError((cause as Error).message);
    } finally {
      setPending(false);
    }
  };

  return (
    <Modal title={`Пароль — ${user.username}`} onClose={onClose}>
      <form onSubmit={handleSubmit}>
        {error && <FormError message={error} />}
        <Field label="Новый пароль">
          <Input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            minLength={8}
            autoFocus
          />
        </Field>
        <div className={styles.actions}>
          <Button variant="outline" type="button" onClick={onClose}>
            Отмена
          </Button>
          <Button variant="pink" type="submit" disabled={pending}>
            {pending ? "Сохраняем…" : "Сменить пароль"}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
