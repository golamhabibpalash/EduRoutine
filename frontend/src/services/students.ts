import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"

export interface CreateStudentPayload {
  student_id: string
  name: string
  email: string
  phone?: string
  batch_id: string
  section_id: string
  enrollment_year: number
  is_active: boolean
}

export const studentsApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    if (p?.filter) params.set("q", p.filter)
    const r = await apiClient.get(`${API_PREFIX}/students?${params}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/students/${id}`)
    return r.data
  },
  create: async (payload: CreateStudentPayload) => {
    const r = await apiClient.post(`${API_PREFIX}/students`, payload)
    return r.data
  },
  update: async (id: string, payload: Partial<CreateStudentPayload>) => {
    const r = await apiClient.put(`${API_PREFIX}/students/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/students/${id}`)
    return r.data
  },
}
