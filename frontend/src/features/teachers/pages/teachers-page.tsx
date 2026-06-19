"use client"

import { useState } from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Plus, Pencil, Trash2, Upload } from "lucide-react"
import { useTeachers, useCreateTeacher, useUpdateTeacher, useDeleteTeacher } from "@/hooks/use-teachers"
import { useDepartments } from "@/hooks/use-academic"
import { useCourses } from "@/hooks/use-courses"
import { TeacherDialog } from "@/features/teachers/components/TeacherDialog"
import { BulkUploadDialog, type FieldMapping } from "@/components/ui/bulk-upload-dialog"
import { bulkUploadApi } from "@/services/upload"
import type { Teacher } from "@/types/teachers"

const teacherFieldMappings: FieldMapping[] = [
  { header: "employee_id", field: "employee_id", required: true },
  { header: "name", field: "name", required: true },
  { header: "email", field: "email", required: true },
  { header: "phone", field: "phone", required: false },
  { header: "department", field: "department", required: true },
  { header: "specialization", field: "specialization", required: false },
  { header: "max_hours_per_week", field: "max_hours_per_week", required: true },
]

export function TeachersPage() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [bulkOpen, setBulkOpen] = useState(false)
  const [editing, setEditing] = useState<Teacher | null>(null)
  const { data, isLoading, refetch } = useTeachers()
  const { data: deptData } = useDepartments()
  const { data: courseData } = useCourses()
  const createMutation = useCreateTeacher()
  const updateMutation = useUpdateTeacher(editing?.id ?? "")
  const deleteMutation = useDeleteTeacher()

  const teachers: Teacher[] = data?.data ?? []
  const departments = deptData?.data ?? []
  const courses = courseData?.data ?? []

  const columns: ColumnDef<Teacher>[] = [
    { accessorKey: "employee_id", header: "Employee ID" },
    { accessorKey: "name", header: "Name" },
    { accessorKey: "email", header: "Email" },
    { accessorKey: "department", header: "Department" },
    { accessorKey: "specialization", header: "Specializations", cell: ({ row }) => (
      <div className="flex flex-wrap gap-1">
        {row.original.specialization.map((s, i) => <Badge key={i} variant="secondary">{s}</Badge>)}
      </div>
    )},
    { accessorKey: "max_hours_per_week", header: "Max Hrs", cell: ({ row }) => <span className="font-mono">{row.original.max_hours_per_week}</span> },
    { accessorKey: "is_active", header: "Status", cell: ({ row }) => row.original.is_active ? <Badge>Active</Badge> : <Badge variant="secondary">Inactive</Badge> },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={() => { if (confirm("Delete this teacher?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
      </div>
    )},
  ]

  function handleSave(data: Parameters<typeof createMutation.mutate>[0]) {
    if (editing) {
      updateMutation.mutate(data, { onSuccess: () => { setDialogOpen(false); setEditing(null) } })
    } else {
      createMutation.mutate(data, { onSuccess: () => setDialogOpen(false) })
    }
  }

  async function handleBulkUpload(items: Record<string, string>[]) {
    return bulkUploadApi.teachers({ items })
  }

  return (
    <div>
      <PageHeader title="Teacher Directory" description="Manage faculty and instructor profiles">
        <Button variant="outline" onClick={() => setBulkOpen(true)}>
          <Upload className="mr-2 h-4 w-4" /> Bulk Upload
        </Button>
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Teacher
        </Button>
      </PageHeader>
      <DataTable columns={columns} data={teachers} searchKey="name" loading={isLoading} />
      <TeacherDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} departments={departments} courses={courses} />
      <BulkUploadDialog
        open={bulkOpen}
        onOpenChange={(v) => { setBulkOpen(v); if (!v) refetch() }}
        title="Bulk Import Teachers"
        description="Upload a CSV file to import multiple teachers at once"
        sampleFilename="teachers-import-template.csv"
        fieldMappings={teacherFieldMappings}
        onUpload={handleBulkUpload}
      />
    </div>
  )
}
