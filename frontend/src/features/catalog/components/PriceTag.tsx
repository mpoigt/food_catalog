import { CURRENCY } from "../../../lib/constants";
import { usePriceUsdOnHover } from "../hooks/usePriceUsdOnHover";
import styles from "./PriceTag.module.css";

type Props = {
  productId: string;
  price: number;
};

function hint(state: ReturnType<typeof usePriceUsdOnHover>["state"]): string {
  switch (state.status) {
    case "ready":
      return `≈ $${state.data.priceUsd.toFixed(2)} по курсу НБ РБ на ${state.data.rateDate}`;
    case "loading":
      return "Считаем курс…";
    case "error":
      return "Курс временно недоступен";
    default:
      return "Наведите, чтобы узнать цену в USD";
  }
}

export function PriceTag({ productId, price }: Props) {
  const { state, start, cancel } = usePriceUsdOnHover(productId);

  return (
    <span className={styles.price}>
      {price} {CURRENCY}
      <span
        className={styles.star}
        onMouseEnter={start}
        onMouseLeave={cancel}
      >
        *<span className={styles.tooltip}>{hint(state)}</span>
      </span>
    </span>
  );
}
