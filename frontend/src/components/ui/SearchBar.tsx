import styles from "./SearchBar.module.css";

type Props = {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
};

export function SearchBar({ value, onChange, placeholder }: Props) {
  return (
    <div className={styles.wrap}>
      <img className={styles.icon} src="/lupa.png" alt="" aria-hidden="true" />
      <input
        className={styles.input}
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder ?? "Поиск продуктов…"}
      />
      {value && (
        <button
          className={styles.clear}
          type="button"
          aria-label="Очистить"
          onClick={() => onChange("")}
        >
          ✕
        </button>
      )}
    </div>
  );
}
