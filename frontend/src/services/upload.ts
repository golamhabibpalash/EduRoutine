import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"

export interface BulkUploadPayload<T> {
  items: T[]
}

export const bulkUploadApi = {
  teachers: async (payload: BulkUploadPayload<Record<string, string>>) => {
    const r = await apiClient.post(`${API_PREFIX}/teachers/bulk`, payload)
    return r.data
  },
  students: async (payload: BulkUploadPayload<Record<string, string>>) => {
    const r = await apiClient.post(`${API_PREFIX}/students/bulk`, payload)
    return r.data
  },
  rooms: async (payload: BulkUploadPayload<Record<string, string>>) => {
    const r = await apiClient.post(`${API_PREFIX}/rooms/bulk`, payload)
    return r.data
  },
  courses: async (payload: BulkUploadPayload<Record<string, string>>) => {
    const r = await apiClient.post(`${API_PREFIX}/courses/bulk`, payload)
    return r.data
  },
}
