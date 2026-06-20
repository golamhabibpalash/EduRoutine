"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import type { AxiosError } from "axios"
import type { ApiError } from "@/types/api"
import {
  sessionsApi, batchesApi, semestersApi, sectionsApi, departmentsApi,
  type CreateDepartmentPayload, type CreateSessionPayload,
  type CreateBatchPayload, type CreateSemesterPayload, type CreateSectionPayload,
} from "@/services/academic"
import type { PaginationParams } from "@/types/api"

// #region Departments
export function useDepartments(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["departments", filters],
    queryFn: () => departmentsApi.list(filters),
  })
}

export function useCreateDepartment() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateDepartmentPayload) => departmentsApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["departments"] }),
  })
}

export function useUpdateDepartment(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateDepartmentPayload) => departmentsApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["departments"] }),
  })
}

export function useDeleteDepartment() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => departmentsApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["departments"] }),
  })
}
// #endregion

// #region Sessions
export function useSessions(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["sessions", filters],
    queryFn: () => sessionsApi.list(filters),
  })
}

export function useCreateSession() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateSessionPayload) => sessionsApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["sessions"] }),
  })
}

export function useUpdateSession(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: Omit<CreateSessionPayload, "is_current">) => sessionsApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["sessions"] }),
  })
}

export function useActivateSession() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => sessionsApi.activate(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["sessions"] }),
  })
}

export function useDeleteSession() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => sessionsApi.delete(id),
    onSuccess: () => {
      toast.success("Session deleted successfully")
      qc.invalidateQueries({ queryKey: ["sessions"] })
    },
    onError: (error: AxiosError<ApiError>) => {
      const message = error.response?.data?.error?.message ?? "Failed to delete session"
      toast.error(message)
    },
  })
}
// #endregion

// #region Batches
export function useBatches(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["batches", filters],
    queryFn: () => batchesApi.list(filters),
  })
}

export function useCreateBatch() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateBatchPayload) => batchesApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["batches"] }),
  })
}

export function useUpdateBatch(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: { name: string; code: string }) => batchesApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["batches"] }),
  })
}

export function useDeleteBatch() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => batchesApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["batches"] }),
  })
}
// #endregion

// #region Semesters
export function useSemesters(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["semesters", filters],
    queryFn: () => semestersApi.list(filters),
  })
}

export function useCreateSemester() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateSemesterPayload) => semestersApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["semesters"] }),
  })
}

export function useUpdateSemester(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: { name: string; number: number; start_date: string; end_date: string }) => semestersApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["semesters"] }),
  })
}

export function useDeleteSemester() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => semestersApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["semesters"] }),
  })
}
// #endregion

// #region Sections
export function useSections(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["sections", filters],
    queryFn: () => sectionsApi.list(filters),
  })
}

export function useCreateSection() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateSectionPayload) => sectionsApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["sections"] }),
  })
}

export function useUpdateSection(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: { name: string; max_capacity: number }) => sectionsApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["sections"] }),
  })
}

export function useDeleteSection() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => sectionsApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["sections"] }),
  })
}
// #endregion
