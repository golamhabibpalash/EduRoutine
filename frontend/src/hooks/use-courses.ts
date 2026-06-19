"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { coursesApi, type CreateCoursePayload, type UpdateCoursePayload } from "@/services/courses"
import type { PaginationParams } from "@/types/api"

export function useCourses(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["courses", filters],
    queryFn: () => coursesApi.list(filters),
  })
}

export function useCourse(id: string) {
  return useQuery({
    queryKey: ["courses", id],
    queryFn: () => coursesApi.get(id),
    enabled: !!id,
  })
}

export function useCreateCourse() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateCoursePayload) => coursesApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["courses"] }),
  })
}

export function useUpdateCourse(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: UpdateCoursePayload) => coursesApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["courses"] }),
  })
}

export function useDeleteCourse() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => coursesApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["courses"] }),
  })
}
