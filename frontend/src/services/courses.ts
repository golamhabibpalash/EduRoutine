import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"

export const coursesApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    if (p?.filter) params.set("q", p.filter)
    const r = await apiClient.get(`${API_PREFIX}/courses?${params}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/courses/${id}`)
    return r.data
  },
}
