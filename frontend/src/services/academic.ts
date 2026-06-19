import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"

export interface CreateDepartmentPayload { name: string; code: string }
export interface CreateSessionPayload { name: string; start_date: string; end_date: string; is_current?: boolean }
export interface CreateBatchPayload { session_id: string; department_id: string; name: string; code: string }
export interface CreateSemesterPayload { session_id: string; name: string; number: number; start_date: string; end_date: string }
export interface CreateSectionPayload { batch_id: string; name: string; max_capacity: number }

function listParams(p?: PaginationParams) {
  const params = new URLSearchParams()
  if (p?.page) params.set("page", String(p.page))
  if (p?.page_size) params.set("page_size", String(p.page_size))
  if (p?.filter) params.set("q", p.filter)
  return params
}

export const departmentsApi = {
  list: async (p?: PaginationParams) => {
    const r = await apiClient.get(`${API_PREFIX}/departments?${listParams(p)}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/departments/${id}`)
    return r.data
  },
  create: async (payload: { name: string; code: string }) => {
    const r = await apiClient.post(`${API_PREFIX}/departments`, payload)
    return r.data
  },
  update: async (id: string, payload: { name: string; code: string }) => {
    const r = await apiClient.put(`${API_PREFIX}/departments/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/departments/${id}`)
    return r.data
  },
}

export const sessionsApi = {
  list: async (p?: PaginationParams) => {
    const r = await apiClient.get(`${API_PREFIX}/sessions?${listParams(p)}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/sessions/${id}`)
    return r.data
  },
  create: async (payload: { name: string; start_date: string; end_date: string; is_current?: boolean }) => {
    const r = await apiClient.post(`${API_PREFIX}/sessions`, payload)
    return r.data
  },
  update: async (id: string, payload: { name: string; start_date: string; end_date: string }) => {
    const r = await apiClient.put(`${API_PREFIX}/sessions/${id}`, payload)
    return r.data
  },
  activate: async (id: string) => {
    const r = await apiClient.patch(`${API_PREFIX}/sessions/${id}/activate`)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/sessions/${id}`)
    return r.data
  },
}

export const semestersApi = {
  list: async (p?: PaginationParams) => {
    const r = await apiClient.get(`${API_PREFIX}/semesters?${listParams(p)}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/semesters/${id}`)
    return r.data
  },
  create: async (payload: { session_id: string; name: string; number: number; start_date: string; end_date: string }) => {
    const r = await apiClient.post(`${API_PREFIX}/semesters`, payload)
    return r.data
  },
  update: async (id: string, payload: { name: string; number: number; start_date: string; end_date: string }) => {
    const r = await apiClient.put(`${API_PREFIX}/semesters/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/semesters/${id}`)
    return r.data
  },
}

export const batchesApi = {
  list: async (p?: PaginationParams) => {
    const r = await apiClient.get(`${API_PREFIX}/batches?${listParams(p)}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/batches/${id}`)
    return r.data
  },
  create: async (payload: { session_id: string; department_id: string; name: string; code: string }) => {
    const r = await apiClient.post(`${API_PREFIX}/batches`, payload)
    return r.data
  },
  update: async (id: string, payload: { name: string; code: string }) => {
    const r = await apiClient.put(`${API_PREFIX}/batches/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/batches/${id}`)
    return r.data
  },
  sections: async (batchId: string) => {
    const r = await apiClient.get(`${API_PREFIX}/batches/${batchId}/sections`)
    return r.data
  },
}

export const sectionsApi = {
  list: async (p?: PaginationParams) => {
    const r = await apiClient.get(`${API_PREFIX}/sections?${listParams(p)}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/sections/${id}`)
    return r.data
  },
  create: async (payload: { batch_id: string; name: string; max_capacity: number }) => {
    const r = await apiClient.post(`${API_PREFIX}/sections`, payload)
    return r.data
  },
  update: async (id: string, payload: { name: string; max_capacity: number }) => {
    const r = await apiClient.put(`${API_PREFIX}/sections/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/sections/${id}`)
    return r.data
  },
}
