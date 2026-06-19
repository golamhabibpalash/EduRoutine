"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { roomsApi, type CreateRoomPayload } from "@/services/rooms"
import type { PaginationParams } from "@/types/api"

export function useRooms(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["rooms", filters],
    queryFn: () => roomsApi.list(filters),
  })
}

export function useRoom(id: string) {
  return useQuery({
    queryKey: ["rooms", id],
    queryFn: () => roomsApi.get(id),
    enabled: !!id,
  })
}

export function useCreateRoom() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateRoomPayload) => roomsApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["rooms"] }),
  })
}

export function useUpdateRoom(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: Partial<CreateRoomPayload>) => roomsApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["rooms"] }),
  })
}

export function useDeleteRoom() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => roomsApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["rooms"] }),
  })
}
