"use client"

import { useState, useMemo } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { TimetableGrid } from "@/features/routines/components/TimetableGrid"
import { SlotDialog } from "@/features/routines/components/SlotDialog"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Play, Archive, Copy, Download } from "lucide-react"
import type { RoutineDetail, DayOfWeek, RoutineStatus } from "@/types/routines"

interface SlotFormData {
  courseCode: string
  courseName: string
  teacherName: string
  roomCode: string
  sectionName: string
  startTime: string
  endTime: string
  isLab: boolean
}

export function RoutineDetailPage() {
  const router = useRouter()
  const [details, setDetails] = useState<RoutineDetail[]>([])
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingSlot, setEditingSlot] = useState<SlotFormData | null>(null)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [pendingDay, setPendingDay] = useState<DayOfWeek | null>(null)
  const [pendingTime, setPendingTime] = useState<string | null>(null)

  const routine = {
    id: "1",
    name: "Sample Routine",
    status: "draft" as "draft" | "published" | "archived",
    session_name: "2026",
    batch_name: "CSE 48",
    semester_name: "6th",
  }

  function handleCellClick(day: DayOfWeek, startTime: string) {
    setEditingSlot(null)
    setEditingId(null)
    setPendingDay(day)
    setPendingTime(startTime)
    setDialogOpen(true)
  }

  function handleCellEdit(detailId: string) {
    const detail = details.find((d) => d.id === detailId)
    if (!detail) return
    setEditingId(detailId)
    setEditingSlot({
      courseCode: detail.course_code ?? "",
      courseName: detail.course_name ?? "",
      teacherName: detail.teacher_name ?? "",
      roomCode: detail.room_code ?? "",
      sectionName: detail.section_name ?? "",
      startTime: detail.start_time,
      endTime: detail.end_time,
      isLab: detail.is_lab,
    })
    setPendingDay(detail.day_of_week)
    setPendingTime(detail.start_time)
    setDialogOpen(true)
  }

  function handleSave(data: SlotFormData) {
    if (editingId) {
      setDetails((prev) =>
        prev.map((d) =>
          d.id === editingId
            ? {
                ...d,
                course_code: data.courseCode,
                course_name: data.courseName,
                teacher_name: data.teacherName,
                room_code: data.roomCode,
                section_name: data.sectionName,
                start_time: data.startTime,
                end_time: data.endTime,
                is_lab: data.isLab,
              }
            : d,
        ),
      )
    } else if (pendingDay && pendingTime) {
      setDetails((prev) => [
        ...prev,
        {
          id: String(Date.now()),
          routine_id: "1",
          course_id: "",
          course_code: data.courseCode,
          course_name: data.courseName,
          teacher_id: "",
          teacher_name: data.teacherName,
          room_id: "",
          room_code: data.roomCode,
          section_id: "",
          section_name: data.sectionName || "A",
          day_of_week: pendingDay,
          time_slot_id: "",
          time_slot_name: "",
          start_time: data.startTime,
          end_time: data.endTime,
          is_lab: data.isLab,
        },
      ])
    }
    setDialogOpen(false)
    setEditingSlot(null)
    setEditingId(null)
    setPendingDay(null)
    setPendingTime(null)
  }

  function handleDelete() {
    if (editingId) {
      setDetails((prev) => prev.filter((d) => d.id !== editingId))
    }
    setDialogOpen(false)
    setEditingSlot(null)
    setEditingId(null)
  }

  const conflictCount = useMemo(() => {
    const seen = new Map<string, string>()
    let count = 0
    for (const d of details) {
      const key = `${d.day_of_week}-${d.start_time}-${d.room_code}`
      if (seen.has(key) && seen.get(key) !== d.teacher_name) count++
      seen.set(key, d.teacher_name ?? "")
    }
    return count
  }, [details])

  return (
    <div className="space-y-6">
      <PageHeader title={routine.name}>
        <Link href="/routines">
          <Button variant="outline">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
        </Link>
      </PageHeader>

      <div className="flex flex-wrap items-center gap-4">
        <Badge variant={routine.status === "published" ? "default" : "secondary"}>
          {routine.status}
        </Badge>
        <span className="text-sm text-muted-foreground">
          {routine.session_name} / {routine.batch_name} / {routine.semester_name}
        </span>
        <span className="text-sm text-muted-foreground">
          {details.length} entries
        </span>
        {conflictCount > 0 && (
          <span className="text-sm font-medium text-destructive">
            {conflictCount} conflict{conflictCount > 1 ? "s" : ""} detected
          </span>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        <Button size="sm">
          <Play className="mr-2 h-4 w-4" />
          Generate
        </Button>
        <Button size="sm" variant="secondary">
          <Download className="mr-2 h-4 w-4" />
          Export
        </Button>
        <Button size="sm" variant="outline">
          <Copy className="mr-2 h-4 w-4" />
          Clone
        </Button>
        <Button size="sm" variant="outline">
          <Archive className="mr-2 h-4 w-4" />
          Archive
        </Button>
      </div>

      <TimetableGrid
        details={details}
        onCellClick={handleCellClick}
        onCellEdit={handleCellEdit}
      />

      <SlotDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        onSave={handleSave}
        onDelete={editingId ? handleDelete : undefined}
        initialData={editingSlot}
        defaultDay={pendingDay}
        defaultStartTime={pendingTime}
      />

      {conflictCount > 0 && (
        <Card className="border-destructive/50">
          <CardHeader>
            <CardTitle className="text-sm text-destructive">Schedule Conflicts</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Room or teacher double-booking detected. Review the highlighted entries and resolve before publishing.
          </CardContent>
        </Card>
      )}
    </div>
  )
}
