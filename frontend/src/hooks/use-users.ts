"use client"

import { useQuery } from "@tanstack/react-query"
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
