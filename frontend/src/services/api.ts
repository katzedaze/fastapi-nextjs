import { Item, ItemCreate, ItemUpdate } from "@/types/item";
import { Order, OrderCreate, OrderUpdate } from "@/types/order";
import { User, UserCreate, UserUpdate } from "@/types/user";
import axios from "axios";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const userApi = {
  /**
   * Get all users
   */
  getUsers: async (): Promise<User[]> => {
    const response = await api.get<User[]>("/users");
    return response.data;
  },

  /**
   * Get user by ID
   */
  getUser: async (id: string): Promise<User> => {
    const response = await api.get<User>(`/users/${id}`);
    return response.data;
  },

  /**
   * Create a new user
   */
  createUser: async (userData: UserCreate): Promise<User> => {
    const response = await api.post<User>("/users", userData);
    return response.data;
  },

  /**
   * Update a user
   */
  updateUser: async (id: string, userData: UserUpdate): Promise<User> => {
    const response = await api.put<User>(`/users/${id}`, userData);
    return response.data;
  },

  /**
   * Delete a user
   */
  deleteUser: async (id: string): Promise<User> => {
    const response = await api.delete<User>(`/users/${id}`);
    return response.data;
  },
};

export const itemApi = {
  /**
   * Get all items
   */
  getItems: async (): Promise<Item[]> => {
    const response = await api.get<Item[]>("/items");
    return response.data;
  },

  /**
   * Get item by ID
   */
  getItem: async (id: string): Promise<Item> => {
    const response = await api.get<Item>(`/items/${id}`);
    return response.data;
  },

  /**
   * Create a new item
   */
  createItem: async (itemData: ItemCreate): Promise<Item> => {
    const response = await api.post<Item>("/items", itemData);
    return response.data;
  },

  /**
   * Update an item
   */
  updateItem: async (id: string, itemData: ItemUpdate): Promise<Item> => {
    const response = await api.put<Item>(`/items/${id}`, itemData);
    return response.data;
  },

  /**
   * Delete an item
   */
  deleteItem: async (id: string): Promise<Item> => {
    const response = await api.delete<Item>(`/items/${id}`);
    return response.data;
  },
};

export const orderApi = {
  /**
   * Get all orders
   */
  getOrders: async (userId?: string): Promise<Order[]> => {
    const url = userId ? `/orders?user_id=${userId}` : "/orders";
    const response = await api.get<Order[]>(url);
    return response.data;
  },

  /**
   * Get order by ID
   */
  getOrder: async (id: string): Promise<Order> => {
    const response = await api.get<Order>(`/orders/${id}`);
    return response.data;
  },

  /**
   * Create a new order
   */
  createOrder: async (orderData: OrderCreate): Promise<Order> => {
    const response = await api.post<Order>("/orders", orderData);
    return response.data;
  },

  /**
   * Update an order
   */
  updateOrder: async (id: string, orderData: OrderUpdate): Promise<Order> => {
    const response = await api.put<Order>(`/orders/${id}`, orderData);
    return response.data;
  },

  /**
   * Delete an order
   */
  deleteOrder: async (id: string): Promise<Order> => {
    const response = await api.delete<Order>(`/orders/${id}`);
    return response.data;
  },
};

export default api;
