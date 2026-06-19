import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"

export interface CreateTeacherPayload {
  employee_id: string
  name: string
  email: string
  phone?: string
  department: string
  specialization: string[]
  max_hours_per_week: number
  is_active: boolean
}

export const teachersApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    if (p?.filter) params.set("q", p.filter)
    const r = await apiClient.get(`${API_PREFIX}/teachers?${params}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/teachers/${id}`)
    return r.data
  },
  create: async (payload: CreateTeacherPayload) => {
    const r = await apiClient.post(`${API_PREFIX}/teachers`, payload)
    return r.data
  },
  update: async (id: string, payload: Partial<CreateTeacherPayload>) => {
    const r = await apiClient.put(`${API_PREFIX}/teachers/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/teachers/${id}`)
    return r.data
  },
}
