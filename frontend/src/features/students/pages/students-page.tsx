"use client"

import { useState } from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Plus, Pencil, Trash2, Upload, Database, Loader2 } from "lucide-react"
import { useStudents, useCreateStudent, useUpdateStudent, useDeleteStudent } from "@/hooks/use-students"
import { StudentDialog } from "@/features/students/components/StudentDialog"
import { BulkUploadDialog, type FieldMapping } from "@/components/ui/bulk-upload-dialog"
import { bulkUploadApi } from "@/services/upload"
import { seedApi } from "@/services/seed"
import type { Student } from "@/types/students"

const studentFieldMappings: FieldMapping[] = [
  { header: "student_id", field: "student_id", required: true },
  { header: "name", field: "name", required: true },
  { header: "email", field: "email", required: true },
  { header: "phone", field: "phone", required: false },
  { header: "batch_id", field: "batch_id", required: true },
  { header: "section_id", field: "section_id", required: true },
  { header: "enrollment_year", field: "enrollment_year", required: true },
]

export function StudentsPage() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [bulkOpen, setBulkOpen] = useState(false)
  const [seeding, setSeeding] = useState(false)
  const [editing, setEditing] = useState<Student | null>(null)
  const { data, isLoading, refetch } = useStudents()
  const createMutation = useCreateStudent()
  const updateMutation = useUpdateStudent(editing?.id ?? "")
  const deleteMutation = useDeleteStudent()

  const students: Student[] = data?.data ?? []

  const columns: ColumnDef<Student>[] = [
    { accessorKey: "student_id", header: "Student ID" },
    { accessorKey: "name", header: "Name" },
    { accessorKey: "email", header: "Email" },
    { accessorKey: "batch_name", header: "Batch" },
    { accessorKey: "section_name", header: "Section" },
    { accessorKey: "enrollment_year", header: "Year", cell: ({ row }) => <span className="font-mono">{row.original.enrollment_year}</span> },
    { accessorKey: "is_active", header: "Status", cell: ({ row }) => row.original.is_active ? <Badge>Active</Badge> : <Badge variant="secondary">Inactive</Badge> },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={() => { if (confirm("Delete this student?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
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
    return bulkUploadApi.students({ items })
  }

  async function handleSeed() {
    setSeeding(true)
    try {
      const result = await seedApi.seed()
      if (result?.status === "success") {
        await refetch()
      }
    } catch (err) {
      console.error("Seed failed:", err)
      alert("Seed failed. Make sure the backend is running (restart it if you just pulled changes).")
    } finally {
      setSeeding(false)
    }
  }

  return (
    <div>
      <PageHeader title="Student Records" description="View and manage student enrollments">
        {students.length === 0 && !isLoading && (
          <Button variant="outline" onClick={handleSeed} disabled={seeding}>
            {seeding ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Database className="mr-2 h-4 w-4" />}
            {seeding ? "Seeding..." : "Load Sample Data"}
          </Button>
        )}
        <Button variant="outline" onClick={() => setBulkOpen(true)}>
          <Upload className="mr-2 h-4 w-4" /> Bulk Upload
        </Button>
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Student
        </Button>
      </PageHeader>
      <DataTable columns={columns} data={students} searchKey="name" loading={isLoading} />
      <StudentDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} />
      <BulkUploadDialog
        open={bulkOpen}
        onOpenChange={(v) => { setBulkOpen(v); if (!v) refetch() }}
        title="Bulk Import Students"
        description="Upload a CSV file to import multiple students at once"
        sampleFilename="students-import-template.csv"
        fieldMappings={studentFieldMappings}
        onUpload={handleBulkUpload}
      />
    </div>
  )
}
