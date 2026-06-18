import { create } from "zustand"
import type { AuthState, User } from "@/types/auth"
import { AUTH_TOKEN_KEY, REFRESH_TOKEN_KEY } from "@/lib/constants"

const COOKIE_PATH = "/"
const COOKIE_MAX_AGE = 7 * 24 * 60 * 60 // 7 days

function setCookie(name: string, value: string) {
  if (typeof document === "undefined") return
  document.cookie = `${name}=${encodeURIComponent(value)}; path=${COOKIE_PATH}; max-age=${COOKIE_MAX_AGE}; SameSite=Lax`
}

function removeCookie(name: string) {
  if (typeof document === "undefined") return
  document.cookie = `${name}=; path=${COOKIE_PATH}; max-age=0`
}

interface AuthActions {
  setUser: (user: User) => void
  setTokens: (accessToken: string, refreshToken: string) => void
  setLoading: (isLoading: boolean) => void
  logout: () => void
  hydrate: () => void
}

export const useAuthStore = create<AuthState & AuthActions>((set) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: true,

  setUser: (user) => set({ user, isAuthenticated: true }),

  setTokens: (accessToken, refreshToken) => {
    localStorage.setItem(AUTH_TOKEN_KEY, accessToken)
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
    setCookie(AUTH_TOKEN_KEY, accessToken)
    set({ accessToken, refreshToken, isAuthenticated: true })
  },

  setLoading: (isLoading) => set({ isLoading }),

  logout: () => {
    localStorage.removeItem(AUTH_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    removeCookie(AUTH_TOKEN_KEY)
    removeCookie(REFRESH_TOKEN_KEY)
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
    })
  },

  hydrate: () => {
    const accessToken = localStorage.getItem(AUTH_TOKEN_KEY)
    const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)
    set({
      accessToken,
      refreshToken,
      isAuthenticated: !!accessToken,
      isLoading: false,
    })
  },
}))
