import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"

export const roomsApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    if (p?.filter) params.set("q", p.filter)
    if (p?.sort_by) params.set("sort", p.sort_by)
    const r = await apiClient.get(`${API_PREFIX}/rooms?${params}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/rooms/${id}`)
    return r.data
  },
}

export const labsApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    const r = await apiClient.get(`${API_PREFIX}/labs?${params}`)
    return r.data
  },
}
