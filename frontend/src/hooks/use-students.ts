"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { studentsApi, type CreateStudentPayload } from "@/services/students"
import type { PaginationParams } from "@/types/api"

export function useStudents(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["students", filters],
    queryFn: () => studentsApi.list(filters),
  })
}

export function useStudent(id: string) {
  return useQuery({
    queryKey: ["students", id],
    queryFn: () => studentsApi.get(id),
    enabled: !!id,
  })
}

export function useCreateStudent() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateStudentPayload) => studentsApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["students"] }),
  })
}

export function useUpdateStudent(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: Partial<CreateStudentPayload>) => studentsApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["students"] }),
  })
}

export function useDeleteStudent() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => studentsApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["students"] }),
  })
}
