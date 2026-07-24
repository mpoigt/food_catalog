import { CURRENCY } from "../../../lib/constants";
import { useCurrency } from "../CurrencyContext";
import styles from "./PriceTag.module.css";

type Props = {
  price: number;
};

export function PriceTag({ price }: Props) {
  const { toUsd, rateDate } = useCurrency();
  const usd = toUsd(price);

  const hint =
    usd !== null
      ? `≈ $${usd.toFixed(2)} по курсу НБ РБ${rateDate ? ` на ${rateDate}` : ""}`
      : "Курс временно недоступен";

  return (
    <span className={styles.price}>
      {price} {CURRENCY}
      <span className={styles.star}>
        *<span className={styles.tooltip}>{hint}</span>
      </span>
    </span>
  );
}
