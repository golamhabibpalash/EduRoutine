"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { sessionsApi, batchesApi, semestersApi, sectionsApi, departmentsApi } from "@/services/academic"
import type { PaginationParams } from "@/types/api"

export function useSessions(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["sessions", filters],
    queryFn: () => sessionsApi.list(filters),
  })
}

export function useBatches(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["batches", filters],
    queryFn: () => batchesApi.list(filters),
  })
}

export function useSemesters(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["semesters", filters],
    queryFn: () => semestersApi.list(filters),
  })
}

export function useSections(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["sections", filters],
    queryFn: () => sectionsApi.list(filters),
  })
}

export function useDepartments(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["departments", filters],
    queryFn: () => departmentsApi.list(filters),
  })
}

export function useCreateSession() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: { name: string; start_date: string; end_date: string; is_current?: boolean }) => sessionsApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["sessions"] }),
  })
}
