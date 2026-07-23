import { CURRENCY } from "../../../lib/constants";
import { useUsdPrice } from "../hooks/useUsdPrice";
import styles from "./PriceTag.module.css";

type Props = {
  productId: string;
  price: number;
};

export function PriceTag({ productId, price }: Props) {
  const { usd, loading, failed, start, cancel } = useUsdPrice(productId);

  const hint = loading
    ? "Загружаем курс…"
    : failed
      ? "Курс недоступен"
      : usd !== null
        ? `≈ $${usd.toFixed(2)} по курсу НБ РБ`
        : "Задержите курсор — покажем в долларах";

  return (
    <span className={styles.price}>
      {price} {CURRENCY}
      <span className={styles.star} onMouseEnter={start} onMouseLeave={cancel}>
        *<span className={styles.tooltip}>{hint}</span>
      </span>
    </span>
  );
}
