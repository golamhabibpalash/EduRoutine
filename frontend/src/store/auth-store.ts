import { create } from "zustand"
import type { AuthState, User } from "@/types/auth"
import { AUTH_TOKEN_KEY, REFRESH_TOKEN_KEY } from "@/lib/constants"

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
    set({ accessToken, refreshToken, isAuthenticated: true })
  },

  setLoading: (isLoading) => set({ isLoading }),

  logout: () => {
    localStorage.removeItem(AUTH_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
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
