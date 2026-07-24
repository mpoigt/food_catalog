import { useState } from "react";
import type { FormEvent } from "react";
import { Button } from "../../../components/ui/Button";
import {
  Field,
  FormError,
  Input,
  Select,
  Textarea,
} from "../../../components/ui/Field";
import { Modal } from "../../../components/ui/Modal";
import {
  createProduct,
  updateProduct,
  uploadProductImage,
} from "../../../api/catalog";
import { useAuth } from "../../auth/AuthContext";
import type { Category, Product } from "../../../types/catalog";
import styles from "./ProductForm.module.css";

type Props = {
  product?: Product;
  categories: Category[];
  onClose: () => void;
  onSaved: () => void;
};

export function ProductForm({ product, categories, onClose, onSaved }: Props) {
  const { canEditSpecialNote } = useAuth();
  const [name, setName] = useState(product?.name ?? "");
  const [categoryId, setCategoryId] = useState(
    product?.categoryId ?? categories[0]?.id ?? "",
  );
  const [description, setDescription] = useState(product?.description ?? "");
  const [price, setPrice] = useState(
    product ? String(product.price) : "",
  );
  const [noteCommon, setNoteCommon] = useState(product?.noteCommon ?? "");
  const [noteSpecial, setNoteSpecial] = useState(product?.noteSpecial ?? "");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  const isEdit = Boolean(product);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setPending(true);
    setError(null);
    try {
      const input = {
        name,
        categoryId,
        description,
        price: Number(price),
        noteCommon: noteCommon || null,
        noteSpecial: canEditSpecialNote ? noteSpecial || null : null,
      };
      const saved = product
        ? await updateProduct(product.id, input)
        : await createProduct(input);
      if (file) {
        await uploadProductImage(saved.id, file);
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
      title={isEdit ? "Изменить продукт" : "Новый продукт"}
      onClose={onClose}
    >
      <form onSubmit={handleSubmit}>
        {error && <FormError message={error} />}

        <Field label="Наименование">
          <Input
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
            maxLength={255}
          />
        </Field>

        <Field label="Категория">
          <Select
            value={categoryId}
            onChange={(event) => setCategoryId(event.target.value)}
            required
          >
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </Select>
        </Field>

        <Field label="Описание">
          <Textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            required
            maxLength={1000}
          />
        </Field>

        <Field label="Стоимость, р">
          <Input
            type="number"
            step="0.01"
            min="0"
            value={price}
            onChange={(event) => setPrice(event.target.value)}
            required
          />
        </Field>

        <Field label="Примечание общее">
          <Input
            value={noteCommon}
            onChange={(event) => setNoteCommon(event.target.value)}
            maxLength={255}
          />
        </Field>

        {canEditSpecialNote && (
          <Field label="Примечание специальное">
            <Input
              value={noteSpecial}
              onChange={(event) => setNoteSpecial(event.target.value)}
              maxLength={255}
            />
          </Field>
        )}

        <Field label="Изображение (JPEG, PNG, WEBP, до 5 МБ)">
          <input
            className={styles.file}
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
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
