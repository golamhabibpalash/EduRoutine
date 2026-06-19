import apiClient from "./api-client"
import { ENDPOINTS } from "@/lib/constants"
import type { User, UserFilters } from "@/types/users"
import type { PaginatedResponse } from "@/types/api"

export const usersApi = {
  list: async (filters?: UserFilters): Promise<PaginatedResponse<User>> => {
    const params = new URLSearchParams()
    if (filters?.search) params.set("q", filters.search)
    if (filters?.is_active !== undefined) params.set("is_active", String(filters.is_active))
    if (filters?.page) params.set("page", String(filters.page))
    if (filters?.page_size) params.set("page_size", String(filters.page_size))
    const response = await apiClient.get(`${ENDPOINTS.users.list}?${params}`)
    return response.data
  },

  get: async (id: string): Promise<User> => {
    const response = await apiClient.get(ENDPOINTS.users.detail(id))
    return response.data
  },

  getMe: async (): Promise<User> => {
    const response = await apiClient.get(ENDPOINTS.users.me)
    return response.data
  },
}
