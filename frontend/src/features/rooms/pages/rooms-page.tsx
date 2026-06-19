"use client"

import { useState } from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Plus, Pencil, Trash2, Upload } from "lucide-react"
import { useRooms, useCreateRoom, useUpdateRoom, useDeleteRoom } from "@/hooks/use-rooms"
import { RoomDialog } from "@/features/rooms/components/RoomDialog"
import { BulkUploadDialog, type FieldMapping } from "@/components/ui/bulk-upload-dialog"
import { bulkUploadApi } from "@/services/upload"
import type { Room } from "@/types/rooms"

const typeLabels: Record<string, string> = {
  classroom: "Classroom", lab: "Lab", lecture_hall: "Lecture Hall",
  seminar_room: "Seminar Room", conference_room: "Conference Room",
}

const roomFieldMappings: FieldMapping[] = [
  { header: "code", field: "code", required: true },
  { header: "name", field: "name", required: true },
  { header: "type", field: "type", required: true },
  { header: "capacity", field: "capacity", required: true },
  { header: "building", field: "building", required: true },
  { header: "floor", field: "floor", required: true },
  { header: "has_projector", field: "has_projector", required: false },
  { header: "has_computers", field: "has_computers", required: false },
  { header: "has_ac", field: "has_ac", required: false },
]

export function RoomsPage() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [bulkOpen, setBulkOpen] = useState(false)
  const [editing, setEditing] = useState<Room | null>(null)
  const { data, isLoading, refetch } = useRooms()
  const createMutation = useCreateRoom()
  const updateMutation = useUpdateRoom(editing?.id ?? "")
  const deleteMutation = useDeleteRoom()

  const rooms: Room[] = data?.data ?? []

  const columns: ColumnDef<Room>[] = [
    { accessorKey: "code", header: "Code" },
    { accessorKey: "name", header: "Name" },
    { accessorKey: "type", header: "Type", cell: ({ getValue }) => typeLabels[getValue<string>()] ?? getValue<string>() },
    { accessorKey: "capacity", header: "Capacity" },
    { accessorKey: "building", header: "Building" },
    { accessorKey: "floor", header: "Floor" },
    { accessorKey: "has_ac", header: "AC", cell: ({ row }) => row.original.has_ac ? <Badge variant="outline">Yes</Badge> : <span className="text-muted-foreground">No</span> },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" onClick={() => { setEditing(row.original); setDialogOpen(true) }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={() => { if (confirm("Delete this room?")) deleteMutation.mutate(row.original.id) }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
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
    return bulkUploadApi.rooms({ items })
  }

  return (
    <div>
      <PageHeader title="Room Inventory" description="Manage classrooms, labs, and facilities">
        <Button variant="outline" onClick={() => setBulkOpen(true)}>
          <Upload className="mr-2 h-4 w-4" /> Bulk Upload
        </Button>
        <Button onClick={() => { setEditing(null); setDialogOpen(true) }}>
          <Plus className="mr-2 h-4 w-4" /> Add Room
        </Button>
      </PageHeader>
      <DataTable columns={columns} data={rooms} searchKey="name" loading={isLoading} />
      <RoomDialog open={dialogOpen} onOpenChange={setDialogOpen} onSave={handleSave} initialData={editing} />
      <BulkUploadDialog
        open={bulkOpen}
        onOpenChange={(v) => { setBulkOpen(v); if (!v) refetch() }}
        title="Bulk Import Rooms"
        description="Upload a CSV file to import multiple rooms at once"
        sampleFilename="rooms-import-template.csv"
        fieldMappings={roomFieldMappings}
        onUpload={handleBulkUpload}
      />
    </div>
  )
}
