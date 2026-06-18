import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"

export const timeSlotsApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    const r = await apiClient.get(`${API_PREFIX}/time-slots?${params}`)
    return r.data
  },
}

export const periodsApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    const r = await apiClient.get(`${API_PREFIX}/periods?${params}`)
    return r.data
  },
}

export const routinesApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    if (p?.filter) params.set("q", p.filter)
    const r = await apiClient.get(`${API_PREFIX}/routines?${params}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/routines/${id}`)
    return r.data
  },
}
