import apiClient from "./api-client"
import { ENDPOINTS } from "@/lib/constants"
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  RefreshRequest,
  RefreshResponse,
} from "@/types/auth"
import type { User } from "@/types/users"

export const authApi = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post(ENDPOINTS.auth.login, data)
    return response.data
  },

  register: async (data: RegisterRequest): Promise<RegisterResponse> => {
    const response = await apiClient.post(ENDPOINTS.auth.register, data)
    return response.data
  },

  refresh: async (data: RefreshRequest): Promise<RefreshResponse> => {
    const response = await apiClient.post(ENDPOINTS.auth.refresh, data)
    return response.data
  },

  logout: async (): Promise<void> => {
    await apiClient.post(ENDPOINTS.auth.logout)
  },

  forgotPassword: async (email: string): Promise<void> => {
    await apiClient.post(ENDPOINTS.auth.forgotPassword, { email })
  },

  resetPassword: async (token: string, password: string): Promise<void> => {
    await apiClient.post(ENDPOINTS.auth.resetPassword, { token, password })
  },

  getMe: async (): Promise<User> => {
    const response = await apiClient.get(ENDPOINTS.users.me)
    return response.data
  },

  getOAuthUrl: (provider: string): string => {
    return `${ENDPOINTS.auth.oauth(provider)}?redirect_uri=${encodeURIComponent(
      `${window.location.origin}/auth/callback`,
    )}`
  },
}
