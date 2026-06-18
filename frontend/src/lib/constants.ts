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
  sessions: {
    list: `${API_PREFIX}/sessions`,
    detail: (id: string) => `${API_PREFIX}/sessions/${id}`,
  },
  batches: {
    list: `${API_PREFIX}/batches`,
    detail: (id: string) => `${API_PREFIX}/batches/${id}`,
  },
  semesters: {
    list: `${API_PREFIX}/semesters`,
    detail: (id: string) => `${API_PREFIX}/semesters/${id}`,
  },
  sections: {
    list: `${API_PREFIX}/sections`,
    detail: (id: string) => `${API_PREFIX}/sections/${id}`,
  },
  courses: {
    list: `${API_PREFIX}/courses`,
    detail: (id: string) => `${API_PREFIX}/courses/${id}`,
  },
  teachers: {
    list: `${API_PREFIX}/teachers`,
    detail: (id: string) => `${API_PREFIX}/teachers/${id}`,
  },
  students: {
    list: `${API_PREFIX}/students`,
    detail: (id: string) => `${API_PREFIX}/students/${id}`,
  },
  rooms: {
    list: `${API_PREFIX}/rooms`,
    detail: (id: string) => `${API_PREFIX}/rooms/${id}`,
  },
  labs: {
    list: `${API_PREFIX}/labs`,
  },
  timeSlots: {
    list: `${API_PREFIX}/time-slots`,
  },
  periods: {
    list: `${API_PREFIX}/periods`,
  },
  routines: {
    list: `${API_PREFIX}/routines`,
    detail: (id: string) => `${API_PREFIX}/routines/${id}`,
  },
  roles: {
    list: `${API_PREFIX}/roles`,
    detail: (id: string) => `${API_PREFIX}/roles/${id}`,
  },
  permissions: {
    list: `${API_PREFIX}/permissions`,
  },
} as const

export const AUTH_TOKEN_KEY = "access_token"
export const REFRESH_TOKEN_KEY = "refresh_token"
