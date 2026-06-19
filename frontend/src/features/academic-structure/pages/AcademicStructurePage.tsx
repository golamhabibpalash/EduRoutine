"use client"

import { useState } from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Plus, Pencil, Trash2, CheckCircle2 } from "lucide-react"
import { DepartmentDialog } from "@/features/academic-structure/components/DepartmentDialog"
import { SessionDialog } from "@/features/academic-structure/components/SessionDialog"
import { BatchDialog } from "@/features/academic-structure/components/BatchDialog"
import { SemesterDialog } from "@/features/academic-structure/components/SemesterDialog"
import { SectionDialog } from "@/features/academic-structure/components/SectionDialog"
import {
  useDepartments, useCreateDepartment, useUpdateDepartment, useDeleteDepartment,
  useSessions, useCreateSession, useUpdateSession, useActivateSession, useDeleteSession,
  useBatches, useCreateBatch, useUpdateBatch, useDeleteBatch,
  useSemesters, useCreateSemester, useUpdateSemester, useDeleteSemester,
  useSections, useCreateSection, useUpdateSection, useDeleteSection,
} from "@/hooks/use-academic"
import type { Department, Session, Batch, Semester, Section } from "@/types/academic"

export function AcademicStructurePage() {
  const [tab, setTab] = useState("departments")

  return (
    <div>
      <PageHeader title="Academic Structure" description="Manage departments, sessions, batches, semesters, and sections">
      </PageHeader>
      <Tabs value={tab} onValueChange={setTab} defaultValue="departments" className="mt-2">
        <TabsList>
          <TabsTrigger value="departments">Departments</TabsTrigger>
          <TabsTrigger value="sessions">Sessions</TabsTrigger>
          <TabsTrigger value="batches">Batches</TabsTrigger>
          <TabsTrigger value="semesters">Semesters</TabsTrigger>
          <TabsTrigger value="sections">Sections</TabsTrigger>
        </TabsList>
        <div className="mt-4">
          <TabsContent value="departments"><DepartmentsTab /></TabsContent>
          <TabsContent value="sessions"><SessionsTab /></TabsContent>
          <TabsContent value="batches"><BatchesTab /></TabsContent>
          <TabsContent value="semesters"><SemestersTab /></TabsContent>
          <TabsContent value="sections"><SectionsTab /></TabsContent>
        </div>
      </Tabs>
    </div>
  )
}

// ============================================================ Departments Tab
function DepartmentsTab() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Department | null>(null)
  const { data, isLoading } = useDepartments()
  const createMutation = useCreateDepartment()
  const updateMutation = useUpdateDepartment(editing?.id ?? "")
  const deleteMutation = useDeleteDepartment()

  const items: Department[] = data?.data ?? []

  const columns: ColumnDef<Department>[] = [
    { accessorKey: "code", header: "Code" },
    { accessorKey: "name", header: "Name" },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={() => { if (confirm("Delete this department?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
      </div>
    )},
  ]

  function handleSave(data: { name: string; code: string }) {
    if (editing) {
      updateMutation.mutate(data, { onSuccess: () => { setDialogOpen(false); setEditing(null) } })
    } else {
      createMutation.mutate(data, { onSuccess: () => setDialogOpen(false) })
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Department
        </Button>
      </div>
      <DataTable columns={columns} data={items} searchKey="name" loading={isLoading} />
      <DepartmentDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} />
    </div>
  )
}

// ============================================================ Sessions Tab
function SessionsTab() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Session | null>(null)
  const { data, isLoading } = useSessions()
  const createMutation = useCreateSession()
  const updateMutation = useUpdateSession(editing?.id ?? "")
  const activateMutation = useActivateSession()
  const deleteMutation = useDeleteSession()

  const items: Session[] = data?.data ?? []

  const columns: ColumnDef<Session>[] = [
    { accessorKey: "name", header: "Name" },
    { accessorKey: "start_date", header: "Start", cell: ({ getValue }) => (getValue() as string).slice(0, 10) },
    { accessorKey: "end_date", header: "End", cell: ({ getValue }) => (getValue() as string).slice(0, 10) },
    { accessorKey: "is_current", header: "Status", cell: ({ row }) => row.original.is_current ? <Badge><CheckCircle2 className="mr-1 h-3 w-3" /> Current</Badge> : <Badge variant="secondary">Inactive</Badge> },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        {!row.original.is_current && (
          <Button size="icon" variant="outline" onClick={() => activateMutation.mutate(row.original.id)} title="Activate"><CheckCircle2 className="h-4 w-4 text-green-600" /></Button>
        )}
        <Button size="icon" variant="ghost" onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={() => { if (confirm("Delete this session?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
      </div>
    )},
  ]

  function handleSave(data: { name: string; start_date: string; end_date: string; is_current: boolean }) {
    if (editing) {
      updateMutation.mutate(data, { onSuccess: () => { setDialogOpen(false); setEditing(null) } })
    } else {
      createMutation.mutate(data, { onSuccess: () => setDialogOpen(false) })
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Session
        </Button>
      </div>
      <DataTable columns={columns} data={items} searchKey="name" loading={isLoading} />
      <SessionDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} />
    </div>
  )
}

// ============================================================ Batches Tab
function BatchesTab() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Batch | null>(null)
  const { data, isLoading } = useBatches()
  const { data: deptData } = useDepartments()
  const { data: sessData } = useSessions()
  const createMutation = useCreateBatch()
  const updateMutation = useUpdateBatch(editing?.id ?? "")
  const deleteMutation = useDeleteBatch()

  const items: Batch[] = data?.data ?? []
  const departments = deptData?.data ?? []
  const sessions = sessData?.data ?? []

  const columns: ColumnDef<Batch>[] = [
    { accessorKey: "code", header: "Code" },
    { accessorKey: "name", header: "Name" },
    { id: "session", header: "Session", cell: ({ row }) => <span className="text-muted-foreground">{sessions.find((s: Session) => s.id === row.original.session_id)?.name ?? row.original.session_id.slice(0, 8)}</span> },
    { id: "department", header: "Department", cell: ({ row }) => <span className="text-muted-foreground">{departments.find((d: Department) => d.id === row.original.department_id)?.code ?? row.original.department_id.slice(0, 8)}</span> },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={() => { if (confirm("Delete this batch?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
      </div>
    )},
  ]

  function handleSave(data: { session_id: string; department_id: string; name: string; code: string }) {
    if (editing) {
      updateMutation.mutate(data, { onSuccess: () => { setDialogOpen(false); setEditing(null) } })
    } else {
      createMutation.mutate(data, { onSuccess: () => setDialogOpen(false) })
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Batch
        </Button>
      </div>
      <DataTable columns={columns} data={items} searchKey="name" loading={isLoading} />
      <BatchDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} departments={departments} sessions={sessions} />
    </div>
  )
}

// ============================================================ Semesters Tab
function SemestersTab() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Semester | null>(null)
  const { data, isLoading } = useSemesters()
  const { data: sessData } = useSessions()
  const createMutation = useCreateSemester()
  const updateMutation = useUpdateSemester(editing?.id ?? "")
  const deleteMutation = useDeleteSemester()

  const items: Semester[] = data?.data ?? []
  const sessions = sessData?.data ?? []

  const columns: ColumnDef<Semester>[] = [
    { accessorKey: "number", header: "#", cell: ({ row }) => <span className="font-mono">{row.original.number}</span> },
    { accessorKey: "name", header: "Name" },
    { id: "session", header: "Session", cell: ({ row }) => <span className="text-muted-foreground">{sessions.find((s: Session) => s.id === row.original.session_id)?.name ?? row.original.session_id.slice(0, 8)}</span> },
    { accessorKey: "start_date", header: "Start", cell: ({ getValue }) => (getValue() as string).slice(0, 10) },
    { accessorKey: "end_date", header: "End", cell: ({ getValue }) => (getValue() as string).slice(0, 10) },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={() => { if (confirm("Delete this semester?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
      </div>
    )},
  ]

  function handleSave(data: { session_id: string; name: string; number: number; start_date: string; end_date: string }) {
    if (editing) {
      updateMutation.mutate(data, { onSuccess: () => { setDialogOpen(false); setEditing(null) } })
    } else {
      createMutation.mutate(data, { onSuccess: () => setDialogOpen(false) })
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Semester
        </Button>
      </div>
      <DataTable columns={columns} data={items} searchKey="name" loading={isLoading} />
      <SemesterDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} sessions={sessions} />
    </div>
  )
}

// ============================================================ Sections Tab
function SectionsTab() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Section | null>(null)
  const { data, isLoading } = useSections()
  const { data: batchData } = useBatches()
  const createMutation = useCreateSection()
  const updateMutation = useUpdateSection(editing?.id ?? "")
  const deleteMutation = useDeleteSection()

  const items: Section[] = data?.data ?? []
  const batches = batchData?.data ?? []

  const columns: ColumnDef<Section>[] = [
    { accessorKey: "name", header: "Name" },
    { id: "batch", header: "Batch", cell: ({ row }) => <span className="text-muted-foreground">{batches.find((b: Batch) => b.id === row.original.batch_id)?.name ?? row.original.batch_id.slice(0, 8)}</span> },
    { accessorKey: "max_capacity", header: "Max Capacity", cell: ({ row }) => <span className="font-mono">{row.original.max_capacity}</span> },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={() => { if (confirm("Delete this section?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
      </div>
    )},
  ]

  function handleSave(data: { batch_id: string; name: string; max_capacity: number }) {
    if (editing) {
      updateMutation.mutate(data, { onSuccess: () => { setDialogOpen(false); setEditing(null) } })
    } else {
      createMutation.mutate(data, { onSuccess: () => setDialogOpen(false) })
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Section
        </Button>
      </div>
      <DataTable columns={columns} data={items} searchKey="name" loading={isLoading} />
      <SectionDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} batches={batches} />
    </div>
  )
}