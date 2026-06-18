export type UserStatus = "active" | "inactive" | "locked" | "suspended"

export interface User {
  id: string
  email: string
  email_verified: boolean
  display_name: string
  phone: string | null
  status: UserStatus
  last_login_at: string | null
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface RegisterRequest {
  email: string
  password: string
  display_name: string
  phone?: string
}

export interface RegisterResponse {
  id: string
  email: string
  display_name: string
  created_at: string
}

export interface RefreshRequest {
  refresh_token: string
}

export interface RefreshResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
}
