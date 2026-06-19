import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"

export interface CreateCoursePayload {
  department_id: string
  code: string
  title: string
  credits: number
  lecture_hours: number
  lab_hours: number
  is_active?: boolean
  prerequisite_ids?: string[]
}

export interface UpdateCoursePayload {
  title: string
  credits: number
  lecture_hours: number
  lab_hours: number
  is_active: boolean
}

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
  create: async (payload: CreateCoursePayload) => {
    const r = await apiClient.post(`${API_PREFIX}/courses`, payload)
    return r.data
  },
  update: async (id: string, payload: UpdateCoursePayload) => {
    const r = await apiClient.put(`${API_PREFIX}/courses/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/courses/${id}`)
    return r.data
  },
}
