export interface Item {
  id: string;
  name: string;
  description: string | null;
  price: number;
  stock: number;
  image_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface ItemCreate {
  name: string;
  description?: string | null;
  price: number;
  stock: number;
  image_url?: string | null;
}

export interface ItemUpdate {
  name?: string;
  description?: string | null;
  price?: number;
  stock?: number;
  image_url?: string | null;
}
