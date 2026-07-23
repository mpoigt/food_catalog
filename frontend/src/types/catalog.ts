export type Category = {
  id: string;
  name: string;
};

export type Product = {
  id: string;
  name: string;
  categoryId: string;
  categoryName: string;
  description: string;
  price: number;
  noteCommon: string | null;
  noteSpecial: string | null;
  image?: string;
};
