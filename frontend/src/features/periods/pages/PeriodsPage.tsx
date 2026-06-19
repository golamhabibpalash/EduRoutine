"use client"

import { useState, useEffect } from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { PageHeader } from "@/components/layout/page-header"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Plus, Pencil, Trash2 } from "lucide-react"
import { periodsApi, type CreatePeriodPayload } from "@/services/routines"
import type { Period } from "@/types/routines"
import type { PaginatedResponse } from "@/types/api"

const DEFAULT_PERIODS: CreatePeriodPayload[] = [
  { name: "1st Period", period_number: 1, start_time: "08:00", end_time: "09:00", duration_minutes: 60, is_break: false },
  { name: "2nd Period", period_number: 2, start_time: "09:00", end_time: "10:00", duration_minutes: 60, is_break: false },
  { name: "3rd Period", period_number: 3, start_time: "10:00", end_time: "11:00", duration_minutes: 60, is_break: false },
  { name: "4th Period", period_number: 4, start_time: "11:00", end_time: "12:00", duration_minutes: 60, is_break: false },
  { name: "Break", period_number: 5, start_time: "12:00", end_time: "13:00", duration_minutes: 60, is_break: true },
  { name: "5th Period", period_number: 6, start_time: "13:00", end_time: "14:00", duration_minutes: 60, is_break: false },
  { name: "6th Period", period_number: 7, start_time: "14:00", end_time: "15:00", duration_minutes: 60, is_break: false },
  { name: "7th Period", period_number: 8, start_time: "15:00", end_time: "16:00", duration_minutes: 60, is_break: false },
  { name: "8th Period", period_number: 9, start_time: "16:00", end_time: "17:00", duration_minutes: 60, is_break: false },
]

export function PeriodsPage() {
  const [data, setData] = useState<PaginatedResponse<Period> | null>(null)
  const [loading, setLoading] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Period | null>(null)
  const [name, setName] = useState("")
  const [startTime, setStartTime] = useState("")
  const [endTime, setEndTime] = useState("")
  const [duration, setDuration] = useState(60)
  const [periodNumber, setPeriodNumber] = useState(1)
  const [isBreak, setIsBreak] = useState(false)
  const [saving, setSaving] = useState(false)

  const periods = data?.data ?? []

  async function load() {
    setLoading(true)
    try {
      const res = await periodsApi.list()
      setData(res)
    } catch {
      setData({ data: [], pagination: { page: 1, page_size: 50, total_items: 0, total_pages: 1, has_next: false, has_previous: false } })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const columns: ColumnDef<Period>[] = [
    { accessorKey: "name", header: "Period" },
    { accessorKey: "start_time", header: "Start", cell: ({ getValue }) => (getValue() as string).slice(0, 5) },
    { accessorKey: "end_time", header: "End", cell: ({ getValue }) => (getValue() as string).slice(0, 5) },
    { accessorKey: "duration_minutes", header: "Duration", cell: ({ row }) => <span className="font-mono">{row.original.duration_minutes} min</span> },
    { id: "actions", cell: ({ row }) => (
      <div className="flex gap-1">
        <Button size="icon" variant="ghost" onClick={() => {
          setEditing(row.original)
          setName(row.original.name)
          setStartTime(row.original.start_time.slice(0, 5))
          setEndTime(row.original.end_time.slice(0, 5))
          setDuration(row.original.duration_minutes)
          setPeriodNumber(row.original.period_number)
          setIsBreak(row.original.is_break)
          setDialogOpen(true)
        }}><Pencil className="h-4 w-4" /></Button>
        <Button size="icon" variant="ghost" onClick={async () => {
          if (confirm("Delete this period?")) {
            await periodsApi.delete(row.original.id)
            load()
          }
        }}><Trash2 className="h-4 w-4 text-destructive" /></Button>
      </div>
    )},
  ]

  function openAdd() {
    setEditing(null)
    setName("")
    setStartTime("")
    setEndTime("")
    setDuration(60)
    setPeriodNumber(periods.length + 1)
    setIsBreak(false)
    setDialogOpen(true)
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    try {
      const payload: CreatePeriodPayload = { name, period_number: periodNumber, start_time: startTime, end_time: endTime, duration_minutes: duration, is_break: isBreak }
      if (editing) {
        await periodsApi.update(editing.id, payload)
      } else {
        await periodsApi.create(payload)
      }
      setDialogOpen(false)
      load()
    } finally {
      setSaving(false)
    }
  }

  async function seedDefaults() {
    for (const p of DEFAULT_PERIODS) {
      try { await periodsApi.create(p) } catch { /* skip duplicates */ }
    }
    load()
  }

  return (
    <div>
      <PageHeader title="Time Periods" description="Configure time slots for class periods">
        <Button variant="outline" onClick={seedDefaults} disabled={periods.length > 0}>
          Seed Defaults
        </Button>
        <Button onClick={openAdd}>
          <Plus className="mr-2 h-4 w-4" /> Add Period
        </Button>
      </PageHeader>

      <DataTable columns={columns} data={periods} loading={loading} pageSize={50} />

      {periods.length === 0 && !loading && (
        <div className="mt-4 rounded-lg border border-dashed p-6 text-center text-sm text-muted-foreground">
          No periods configured. Click <strong>Seed Defaults</strong> to create standard 9-period schedule
          (8:00 AM – 5:00 PM), or <strong>Add Period</strong> to create custom slots.
        </div>
      )}

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="sm:max-w-sm">
          <DialogHeader>
            <DialogTitle>{editing ? "Edit Period" : "Add Period"}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSave} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Period Name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="1st Period" required />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-2">
                <Label htmlFor="startTime">Start Time</Label>
                <Input id="startTime" type="time" value={startTime} onChange={(e) => setStartTime(e.target.value)} required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="endTime">End Time</Label>
                <Input id="endTime" type="time" value={endTime} onChange={(e) => setEndTime(e.target.value)} required />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="periodNumber">Period Number</Label>
              <Input id="periodNumber" type="number" value={periodNumber} onChange={(e) => setPeriodNumber(Number(e.target.value))} min={1} max={30} />
            </div>
            <div className="flex items-center gap-2">
              <Checkbox id="isBreak" checked={isBreak} onCheckedChange={(v) => setIsBreak(v === true)} />
              <Label htmlFor="isBreak">Break period</Label>
            </div>
            <div className="space-y-2">
              <Label htmlFor="duration">Duration (minutes)</Label>
              <Input id="duration" type="number" value={duration} onChange={(e) => setDuration(Number(e.target.value))} min={5} max={180} />
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
              <Button type="submit" disabled={saving}>{saving ? "Saving..." : editing ? "Update" : "Create"}</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}
