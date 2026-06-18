import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { Session, Batch, Semester, Section } from "@/types/academic"
import type { PaginationParams } from "@/types/api"

function listParams(p?: PaginationParams) {
  const params = new URLSearchParams()
  if (p?.page) params.set("page", String(p.page))
  if (p?.page_size) params.set("page_size", String(p.page_size))
  if (p?.sort_by) params.set("sort", p.sort_by)
  if (p?.filter) params.set("q", p.filter)
  return params
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
}
