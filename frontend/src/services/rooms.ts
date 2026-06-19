import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"
import type { PaginationParams } from "@/types/api"
import type { RoomType } from "@/types/rooms"

export interface CreateRoomPayload {
  code: string
  name: string
  type: RoomType
  capacity: number
  building: string
  floor: number
  has_projector: boolean
  has_computers: boolean
  has_ac: boolean
  is_active: boolean
}

export const roomsApi = {
  list: async (p?: PaginationParams) => {
    const params = new URLSearchParams()
    if (p?.page) params.set("page", String(p.page))
    if (p?.page_size) params.set("page_size", String(p.page_size))
    if (p?.filter) params.set("q", p.filter)
    const r = await apiClient.get(`${API_PREFIX}/rooms?${params}`)
    return r.data
  },
  get: async (id: string) => {
    const r = await apiClient.get(`${API_PREFIX}/rooms/${id}`)
    return r.data
  },
  create: async (payload: CreateRoomPayload) => {
    const r = await apiClient.post(`${API_PREFIX}/rooms`, payload)
    return r.data
  },
  update: async (id: string, payload: Partial<CreateRoomPayload>) => {
    const r = await apiClient.put(`${API_PREFIX}/rooms/${id}`, payload)
    return r.data
  },
  delete: async (id: string) => {
    const r = await apiClient.delete(`${API_PREFIX}/rooms/${id}`)
    return r.data
  },
}
