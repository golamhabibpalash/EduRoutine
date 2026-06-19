"use client"

import { useState } from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Plus, Pencil, Trash2 } from "lucide-react"
import { useRoles, usePermissions, useCreateRole, useUpdateRole, useDeleteRole } from "@/hooks/use-roles"
import { RoleDialog } from "@/features/roles/components/RoleDialog"
import type { Role } from "@/types/roles"

export function RolesPage() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Role | null>(null)
  const { data, isLoading } = useRoles()
  const { data: permData } = usePermissions()
  const createMutation = useCreateRole()
  const updateMutation = useUpdateRole(editing?.id ?? "")
  const deleteMutation = useDeleteRole()

  const roles: Role[] = data?.data ?? []
  const permissions = permData?.data ?? []

  const columns: ColumnDef<Role>[] = [
    { accessorKey: "name", header: "Role" },
    { accessorKey: "description", header: "Description", cell: ({ getValue }) => (getValue() as string) ?? "\u2014" },
    { accessorKey: "permission_count", header: "Permissions", cell: ({ row }) => <Badge variant="secondary">{row.original.permission_count}</Badge> },
    { accessorKey: "is_system_role", header: "Type", cell: ({ row }) => row.original.is_system_role ? <Badge>System</Badge> : <Badge variant="outline">Custom</Badge> },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" disabled={row.original.is_system_role} onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" disabled={row.original.is_system_role} onClick={() => { if (confirm("Delete this role?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
      </div>
    )},
  ]

  function handleSave(data: { name: string; description: string; permission_ids: string[] }) {
    if (editing) {
      updateMutation.mutate(data, { onSuccess: () => { setDialogOpen(false); setEditing(null) } })
    } else {
      createMutation.mutate(data, { onSuccess: () => setDialogOpen(false) })
    }
  }

  return (
    <div>
      <PageHeader title="Roles & Permissions" description="Manage user roles and their permissions">
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Role
        </Button>
      </PageHeader>
      <DataTable columns={columns} data={roles} searchKey="name" loading={isLoading} />
      <RoleDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} permissions={permissions} />
    </div>
  )
}