import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"

export interface CreateRolePayload {
  name: string
  description?: string
  permission_ids: string[]
}

export const rolesApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    if (p?.filter) params.set("q", p.filter)
    const r = await apiClient.get(`${API_PREFIX}/roles?${params}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/roles/${id}`)
    return r.data
  },
  create: async (payload: CreateRolePayload) => {
    const r = await apiClient.post(`${API_PREFIX}/roles`, payload)
    return r.data
  },
  update: async (id: string, payload: Partial<CreateRolePayload>) => {
    const r = await apiClient.put(`${API_PREFIX}/roles/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/roles/${id}`)
    return r.data
  },
}

export const permissionsApi = {
  list: async () => {
    const r = await apiClient.get(`${API_PREFIX}/permissions`)
    return r.data
  },
}