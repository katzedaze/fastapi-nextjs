export enum OrderStatus {
  PENDING = "pending",
  PROCESSING = "processing",
  SHIPPED = "shipped",
  DELIVERED = "delivered",
  CANCELLED = "cancelled"
}

export interface OrderItem {
  order_id: string;
  item_id: string;
  quantity: number;
  price_at_time: number;
}

export interface OrderItemCreate {
  item_id: string;
  quantity: number;
  price_at_time?: number;
}

export interface Order {
  id: string;
  user_id: string;
  status: OrderStatus;
  shipping_address: string | null;
  total_amount: number;
  notes: string | null;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export interface OrderCreate {
  user_id: string;
  status?: OrderStatus;
  shipping_address?: string | null;
  total_amount: number;
  notes?: string | null;
  items: OrderItemCreate[];
}

export interface OrderUpdate {
  status?: OrderStatus;
  shipping_address?: string | null;
  notes?: string | null;
}