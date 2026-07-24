import { useState } from "react";
import type { FormEvent } from "react";
import { Button } from "../../../components/ui/Button";
import { Field, FormError, Input } from "../../../components/ui/Field";
import { Modal } from "../../../components/ui/Modal";
import { createCategory, updateCategory } from "../../../api/catalog";
import type { Category } from "../../../types/catalog";
import styles from "./ProductForm.module.css";

type Props = {
  category?: Category;
  onClose: () => void;
  onSaved: () => void;
};

export function CategoryForm({ category, onClose, onSaved }: Props) {
  const [name, setName] = useState(category?.name ?? "");
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setPending(true);
    setError(null);
    try {
      if (category) {
        await updateCategory(category.id, name);
      } else {
        await createCategory(name);
      }
      onSaved();
      onClose();
    } catch (cause) {
      setError((cause as Error).message);
    } finally {
      setPending(false);
    }
  };

  return (
    <Modal
      title={category ? "Изменить категорию" : "Новая категория"}
      onClose={onClose}
    >
      <form onSubmit={handleSubmit}>
        {error && <FormError message={error} />}
        <Field label="Название">
          <Input
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
            maxLength={100}
            autoFocus
          />
        </Field>
        <div className={styles.actions}>
          <Button variant="outline" type="button" onClick={onClose}>
            Отмена
          </Button>
          <Button variant="pink" type="submit" disabled={pending}>
            {pending ? "Сохраняем…" : "Сохранить"}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
