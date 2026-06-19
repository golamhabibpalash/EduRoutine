"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { teachersApi, type CreateTeacherPayload } from "@/services/teachers"
import type { PaginationParams } from "@/types/api"

export function useTeachers(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["teachers", filters],
    queryFn: () => teachersApi.list(filters),
  })
}

export function useTeacher(id: string) {
  return useQuery({
    queryKey: ["teachers", id],
    queryFn: () => teachersApi.get(id),
    enabled: !!id,
  })
}

export function useCreateTeacher() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateTeacherPayload) => teachersApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["teachers"] }),
  })
}

export function useUpdateTeacher(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: Partial<CreateTeacherPayload>) => teachersApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["teachers"] }),
  })
}

export function useDeleteTeacher() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => teachersApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["teachers"] }),
  })
}
