import { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "../../../components/ui/Button";
import { Chip } from "../../../components/ui/Chip";
import styles from "./Hero.module.css";

const CANDY_SRC = "/candy.png";

export function Hero() {
  const [hasCandy, setHasCandy] = useState(true);

  return (
    <section className={styles.hero}>
      <div className={styles.content}>
        <Chip tone="pink">Твой продуктовый выбор ♥</Chip>
        <h1 className={styles.title}>
          Продукты, вкус
          <br />и настроение
          <br />
          на каждый день
        </h1>
        <p className={styles.subtitle}>
          Свежие продукты, честные цены и удобный каталог — всё, что нужно,
          чтобы собрать корзину за пару минут.
        </p>
        <div className={styles.actions}>
          <Link to="/">
            <Button variant="pink">Смотреть продукты →</Button>
          </Link>
          <Link to="/categories">
            <Button variant="outline">Категории</Button>
          </Link>
        </div>
      </div>

      <div className={styles.art}>
        <span className={styles.blobPink} />
        {hasCandy ? (
          <img
            className={styles.candy}
            src={CANDY_SRC}
            alt=""
            onError={() => setHasCandy(false)}
          />
        ) : (
          <span className={styles.emoji}>🍬</span>
        )}
      </div>
    </section>
  );
}
