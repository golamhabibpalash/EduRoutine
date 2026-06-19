"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { usersApi } from "@/services/users"
import type { UserFilters } from "@/types/users"

export function useUsers(filters?: UserFilters) {
  return useQuery({
    queryKey: ["users", filters],
    queryFn: () => usersApi.list(filters),
  })
}

export function useUser(id: string) {
  return useQuery({
    queryKey: ["users", id],
    queryFn: () => usersApi.get(id),
    enabled: !!id,
  })
}

export function useUserRoles(id: string) {
  return useQuery({
    queryKey: ["users", id, "roles"],
    queryFn: () => usersApi.getRoles(id),
    enabled: !!id,
  })
}

export function useAssignRoles() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ userId, roleIds }: { userId: string; roleIds: string[] }) => usersApi.assignRoles(userId, roleIds),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["users"] })
    },
  })
}
