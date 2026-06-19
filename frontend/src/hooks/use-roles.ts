"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { rolesApi, permissionsApi, type CreateRolePayload } from "@/services/roles"
import type { PaginationParams } from "@/types/api"

export function useRoles(filters?: PaginationParams) {
  return useQuery({
    queryKey: ["roles", filters],
    queryFn: () => rolesApi.list(filters),
  })
}

export function useRole(id: string) {
  return useQuery({
    queryKey: ["roles", id],
    queryFn: () => rolesApi.get(id),
    enabled: !!id,
  })
}

export function usePermissions() {
  return useQuery({
    queryKey: ["permissions"],
    queryFn: () => permissionsApi.list(),
  })
}

export function useCreateRole() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateRolePayload) => rolesApi.create(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["roles"] }),
  })
}

export function useUpdateRole(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload: Partial<CreateRolePayload>) => rolesApi.update(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["roles"] }),
  })
}

export function useDeleteRole() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => rolesApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["roles"] }),
  })
}