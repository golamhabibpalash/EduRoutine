"use client"

import { useState } from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Plus, Pencil, Trash2, Upload } from "lucide-react"
import { useCourses, useCreateCourse, useUpdateCourse, useDeleteCourse } from "@/hooks/use-courses"
import { CourseDialog } from "@/features/courses/components/CourseDialog"
import { BulkUploadDialog, type FieldMapping } from "@/components/ui/bulk-upload-dialog"
import { bulkUploadApi } from "@/services/upload"
import type { Course } from "@/types/academic"

const courseFieldMappings: FieldMapping[] = [
  { header: "department_id", field: "department_id", required: true },
  { header: "code", field: "code", required: true },
  { header: "title", field: "title", required: true },
  { header: "credits", field: "credits", required: true },
  { header: "lecture_hours", field: "lecture_hours", required: true },
  { header: "lab_hours", field: "lab_hours", required: true },
]

export function CoursesPage() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [bulkOpen, setBulkOpen] = useState(false)
  const [editing, setEditing] = useState<Course | null>(null)
  const { data, isLoading, refetch } = useCourses()
  const createMutation = useCreateCourse()
  const updateMutation = useUpdateCourse(editing?.id ?? "")
  const deleteMutation = useDeleteCourse()

  const courses: Course[] = data?.data ?? []

  const columns: ColumnDef<Course>[] = [
    { accessorKey: "code", header: "Code" },
    { accessorKey: "title", header: "Title" },
    { accessorKey: "credits", header: "Credits", cell: ({ row }) => <span className="font-mono">{row.original.credits}</span> },
    { accessorKey: "lecture_hours", header: "Lecture" },
    { accessorKey: "lab_hours", header: "Lab" },
    { accessorKey: "is_active", header: "Status", cell: ({ row }) => row.original.is_active ? <Badge>Active</Badge> : <Badge variant="secondary">Inactive</Badge> },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={() => { if (confirm("Delete this course?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
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
    return bulkUploadApi.courses({ items })
  }

  return (
    <div>
      <PageHeader title="Course Catalog" description="Create and manage course offerings">
        <Button variant="outline" onClick={() => setBulkOpen(true)}>
          <Upload className="mr-2 h-4 w-4" /> Bulk Upload
        </Button>
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Course
        </Button>
      </PageHeader>
      <DataTable columns={columns} data={courses} searchKey="title" loading={isLoading} />
      <CourseDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} />
      <BulkUploadDialog
        open={bulkOpen}
        onOpenChange={(v) => { setBulkOpen(v); if (!v) refetch() }}
        title="Bulk Import Courses"
        description="Upload a CSV file to import multiple courses at once"
        sampleFilename="courses-import-template.csv"
        fieldMappings={courseFieldMappings}
        onUpload={handleBulkUpload}
      />
    </div>
  )
}
