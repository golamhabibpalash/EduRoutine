"use client"

import { useMemo } from "react"
import Link from "next/link"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { UserPlus } from "lucide-react"
import type { User } from "@/types/users"
import { useUsers } from "@/hooks/use-users"

const statusVariant: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  active: "default",
  inactive: "secondary",
  suspended: "destructive",
  locked: "outline",
}

const columns: ColumnDef<User>[] = [
  {
    accessorKey: "display_name",
    header: "Name",
    cell: ({ row }) => (
      <Link href={`/users/${row.original.id}`} className="font-medium hover:text-primary">
        {row.original.display_name}
      </Link>
    ),
  },
  {
    accessorKey: "email",
    header: "Email",
  },
  {
    accessorKey: "phone",
    header: "Phone",
    cell: ({ getValue }) => getValue<string | null>() ?? "—",
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => (
      <Badge variant={statusVariant[row.original.status] ?? "outline"}>
        {row.original.status}
      </Badge>
    ),
  },
  {
    accessorKey: "email_verified",
    header: "Verified",
    cell: ({ row }) => (row.original.email_verified ? "Yes" : "No"),
  },
  {
    accessorKey: "last_login_at",
    header: "Last Login",
    cell: ({ getValue }) => {
      const val = getValue<string | null>()
      return val ? new Date(val).toLocaleDateString() : "Never"
    },
  },
]

export function UsersPage() {
  const { data, isLoading } = useUsers()

  const users = useMemo(() => data?.data ?? [], [data])

  return (
    <div>
      <PageHeader
        title="Users"
        description="Manage system users and their access"
      >
        <Button disabled>
          <UserPlus className="mr-2 h-4 w-4" />
          Add User
        </Button>
      </PageHeader>

      <DataTable
        columns={columns}
        data={users}
        searchKey="display_name"
        searchPlaceholder="Search by name..."
        loading={isLoading}
      />
    </div>
  )
}
