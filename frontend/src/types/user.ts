export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  email: string;
  full_name: string;
  password: string;
  is_active?: boolean;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
}