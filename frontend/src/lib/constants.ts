export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
export const API_PREFIX = "/api/v1"

export const ENDPOINTS = {
  auth: {
    register: `${API_PREFIX}/auth/register`,
    login: `${API_PREFIX}/auth/login`,
    refresh: `${API_PREFIX}/auth/refresh`,
    logout: `${API_PREFIX}/auth/logout`,
    forgotPassword: `${API_PREFIX}/auth/forgot-password`,
    resetPassword: `${API_PREFIX}/auth/reset-password`,
    oauth: (provider: string) => `${API_PREFIX}/auth/oauth/${provider}`,
    oauthCallback: (provider: string) => `${API_PREFIX}/auth/oauth/${provider}/callback`,
  },
  users: {
    me: `${API_PREFIX}/users/me`,
    list: `${API_PREFIX}/users`,
    detail: (id: string) => `${API_PREFIX}/users/${id}`,
  },
} as const

export const AUTH_TOKEN_KEY = "access_token"
export const REFRESH_TOKEN_KEY = "refresh_token"
