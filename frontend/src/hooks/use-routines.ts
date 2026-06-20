"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { routinesApi, type CreateRoutinePayload, type CreateDetailPayload } from "@/services/routines"
import type { PaginationParams } from "@/types/api"

// #region Routines
export function useRoutines(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["routines", filters],
    queryFn: () => routinesApi.list(filters),
  })
}

export function useRoutine(id: string) {
  return useQuery({
    queryKey: ["routines", id],
    queryFn: () => routinesApi.get(id),
    enabled: !!id,
  })
}

export function useCreateRoutine() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateRoutinePayload) => routinesApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["routines"] }),
  })
}

export function useUpdateRoutine(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: Partial<CreateRoutinePayload>) => routinesApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["routines"] }),
  })
}

export function useDeleteRoutine() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => routinesApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["routines"] }),
  })
}

export function usePublishRoutine() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => routinesApi.publish(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["routines"] }),
  })
}

export function useArchiveRoutine() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => routinesApi.archive(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["routines"] }),
  })
}

export function useCloneRoutine() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => routinesApi.clone(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["routines"] }),
  })
}
// #endregion

// #region Routine Details
export function useRoutineDetails(routineId: string) {
  return useQuery({
    queryKey: ["routine-details", routineId],
    queryFn: () => routinesApi.details.list(routineId),
    enabled: !!routineId,
  })
}

export function useCreateDetail() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateDetailPayload) => routinesApi.details.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["routine-details"], refetchType: "active" }),
  })
}

export function useUpdateDetail(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: Partial<CreateDetailPayload>) => routinesApi.details.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["routine-details"], refetchType: "active" }),
  })
}

export function useDeleteDetail() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => routinesApi.details.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["routine-details"], refetchType: "active" }),
  })
}
// #endregion