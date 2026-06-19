"use client"

import Link from "next/link"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Plus, Eye, Pencil, Trash2 } from "lucide-react"
import { useRoutines, useDeleteRoutine } from "@/hooks/use-routines"
import type { Routine } from "@/types/routines"

const statusVariant: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  draft: "secondary",
  published: "default",
  archived: "outline",
}

export function RoutinesPage() {
  const { data, isLoading, refetch } = useRoutines()
  const deleteMutation = useDeleteRoutine()
  const routines: Routine[] = data?.data ?? []

  const columns: ColumnDef<Routine>[] = [
    {
      accessorKey: "name",
      header: "Name",
      cell: ({ row }) => (
        <Link href={`/routines/${row.original.id}`} className="font-medium hover:text-primary">
          {row.original.name}
        </Link>
      ),
    },
    {
      accessorKey: "department_name",
      header: "Department",
    },
    {
      accessorKey: "session_name",
      header: "Session",
    },
    {
      accessorKey: "batch_name",
      header: "Batch",
    },
    {
      accessorKey: "semester_name",
      header: "Semester",
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
      accessorKey: "version",
      header: "Version",
    },
    {
      accessorKey: "published_at",
      header: "Published",
      cell: ({ getValue }) => {
        const val = getValue<string | null>()
        return val ? new Date(val).toLocaleDateString() : "\u2014"
      },
    },
    {
      id: "actions",
      header: "Actions",
      cell: ({ row }) => (
        <div className="flex gap-1">
          <Link
            href={`/routines/${row.original.id}`}
            className="inline-flex size-8 items-center justify-center rounded-md hover:bg-muted"
            title="View details"
          >
            <Eye className="h-4 w-4" />
          </Link>
          <Link
            href={`/routines/${row.original.id}/edit`}
            className="inline-flex size-8 items-center justify-center rounded-md hover:bg-muted"
            title="Edit"
          >
            <Pencil className="h-4 w-4" />
          </Link>
          <button
            type="button"
            className="inline-flex size-8 items-center justify-center rounded-md hover:bg-muted"
            title="Delete"
            onClick={() => { if (confirm("Delete this routine?")) deleteMutation.mutate(row.original.id, { onSuccess: () => refetch() }) }}
          >
            <Trash2 className="h-4 w-4 text-destructive" />
          </button>
        </div>
      ),
    },
  ]

  return (
    <div>
      <PageHeader
        title="Routines"
        description="Create and manage academic timetables"
      >
        <Link href="/routines/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            New Routine
          </Button>
        </Link>
      </PageHeader>

      <DataTable
        columns={columns}
        data={routines}
        searchKey="name"
        searchPlaceholder="Search by name..."
        loading={isLoading}
      />
    </div>
  )
}