import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"

export interface CreatePeriodPayload {
  name: string
  start_time: string
  end_time: string
  duration_minutes: number
}

export const timeSlotsApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    const r = await apiClient.get(`${API_PREFIX}/time-slots?${params}`)
    return r.data
  },
  create: async (payload: { name: string; start_time: string; end_time: string; slot_count?: number }) => {
    const r = await apiClient.post(`${API_PREFIX}/time-slots`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/time-slots/${id}`)
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
  create: async (payload: CreatePeriodPayload) => {
    const r = await apiClient.post(`${API_PREFIX}/periods`, payload)
    return r.data
  },
  update: async (id: string, payload: Partial<CreatePeriodPayload>) => {
    const r = await apiClient.put(`${API_PREFIX}/periods/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/periods/${id}`)
    return r.data
  },
}

export interface CreateRoutinePayload {
  name: string
  session_id: string
  batch_id: string
  semester_id: string
  department_id: string
}

export interface CreateDetailPayload {
  routine_id: string
  course_id: string
  teacher_id: string
  room_id: string
  section_id: string
  day_of_week: string
  start_time: string
  end_time: string
  is_lab: boolean
  course_code?: string
  course_name?: string
  teacher_name?: string
  room_code?: string
  section_name?: string
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
  create: async (payload: CreateRoutinePayload) => {
    const r = await apiClient.post(`${API_PREFIX}/routines`, payload)
    return r.data
  },
  update: async (id: string, payload: Partial<CreateRoutinePayload>) => {
    const r = await apiClient.put(`${API_PREFIX}/routines/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/routines/${id}`)
    return r.data
  },
  publish: async (id: string) => {
    const r = await apiClient.post(`${API_PREFIX}/routines/${id}/publish`)
    return r.data
  },
  archive: async (id: string) => {
    const r = await apiClient.post(`${API_PREFIX}/routines/${id}/archive`)
    return r.data
  },
  clone: async (id: string) => {
    const r = await apiClient.post(`${API_PREFIX}/routines/${id}/clone`)
    return r.data
  },
  details: {
    list: async (routineId: string) => {
      const r = await apiClient.get(`${API_PREFIX}/routines/${routineId}/details`)
      return r.data
    },
    create: async (payload: CreateDetailPayload) => {
      const r = await apiClient.post(`${API_PREFIX}/routine-details`, payload)
      return r.data
    },
    update: async (id: string, payload: Partial<CreateDetailPayload>) => {
      const r = await apiClient.put(`${API_PREFIX}/routine-details/${id}`, payload)
      return r.data
    },
    delete: async (id: string) => {
      const r = await apiClient.delete(`${API_PREFIX}/routine-details/${id}`)
      return r.data
    },
  },
}
