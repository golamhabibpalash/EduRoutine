"use client"

import Link from "next/link"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import type { Routine } from "@/types/routines"

const statusVariant: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  draft: "secondary",
  published: "default",
  archived: "outline",
}

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
]

export function RoutinesPage() {
  const data: Routine[] = []

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
        data={data}
        searchKey="name"
        searchPlaceholder="Search by name..."
        loading={false}
      />
    </div>
  )
}
