"use client"

import { useState, useMemo } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useQuery } from "@tanstack/react-query"
import { TimetableGrid } from "@/features/routines/components/TimetableGrid"
import { SlotDialog } from "@/features/routines/components/SlotDialog"
import { PageHeader } from "@/components/layout/page-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Play, Archive, Copy, Download, Trash2 } from "lucide-react"
import { useRoutine, useRoutineDetails, usePublishRoutine, useArchiveRoutine, useCloneRoutine, useDeleteRoutine, useCreateDetail, useUpdateDetail, useDeleteDetail } from "@/hooks/use-routines"
import { useCourses } from "@/hooks/use-courses"
import { useTeachers } from "@/hooks/use-teachers"
import { useRooms } from "@/hooks/use-rooms"
import { useSections } from "@/hooks/use-academic"
import { periodsApi } from "@/services/routines"
import { exportToPdf, exportToExcel } from "@/lib/export"
import type { RoutineDetail, DayOfWeek, RoutineConflict } from "@/types/routines"
import type { Period } from "@/types/routines"
import type { Course } from "@/types/academic"
import type { SlotFormData } from "@/features/routines/components/SlotDialog"

interface RoutineDetailPageProps {
  routineId: string
}

export function RoutineDetailPage({ routineId }: RoutineDetailPageProps) {
  const router = useRouter()
  const { data: routineData, isLoading: routineLoading } = useRoutine(routineId)
  const { data: detailsData, isLoading: detailsLoading } = useRoutineDetails(routineId)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingSlot, setEditingSlot] = useState<SlotFormData | null>(null)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [pendingDay, setPendingDay] = useState<DayOfWeek | null>(null)
  const [pendingTime, setPendingTime] = useState<string | null>(null)

  const publishMutation = usePublishRoutine()
  const archiveMutation = useArchiveRoutine()
  const cloneMutation = useCloneRoutine()
  const deleteMutation = useDeleteRoutine()
  const createDetailMutation = useCreateDetail()
  const updateDetailMutation = useUpdateDetail(editingId ?? "")
  const deleteDetailMutation = useDeleteDetail()

  const routine = routineData
  const details: RoutineDetail[] = detailsData?.data ?? []
  const loading = routineLoading || detailsLoading

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
      course_id: detail.course_id,
      course_code: detail.course_code ?? "",
      course_name: detail.course_name ?? "",
      teacher_id: detail.teacher_id,
      teacher_name: detail.teacher_name ?? "",
      room_id: detail.room_id,
      room_code: detail.room_code ?? "",
      section_id: detail.section_id,
      section_name: detail.section_name ?? "",
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
      updateDetailMutation.mutate({
        course_id: data.course_id,
        teacher_id: data.teacher_id,
        room_id: data.room_id,
        section_id: data.section_id,
        start_time: data.startTime,
        end_time: data.endTime,
        is_lab: data.isLab,
      }, {
        onSuccess: () => {
          setDialogOpen(false)
          setEditingSlot(null)
          setEditingId(null)
          setPendingDay(null)
          setPendingTime(null)
        },
      })
    } else if (pendingDay && pendingTime) {
      createDetailMutation.mutate({
        routine_id: routineId,
        course_id: data.course_id,
        teacher_id: data.teacher_id,
        room_id: data.room_id,
        section_id: data.section_id,
        day_of_week: pendingDay,
        start_time: data.startTime,
        end_time: data.endTime,
        is_lab: data.isLab,
      }, {
        onSuccess: () => {
          setDialogOpen(false)
          setEditingSlot(null)
          setEditingId(null)
          setPendingDay(null)
          setPendingTime(null)
        },
      })
    }
  }

  function handleDelete() {
    if (editingId) {
      deleteDetailMutation.mutate(editingId, {
        onSuccess: () => {
          setDialogOpen(false)
          setEditingSlot(null)
          setEditingId(null)
          setPendingDay(null)
          setPendingTime(null)
        },
      })
    }
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

  const { data: coursesData } = useCourses()
  const { data: teachersData } = useTeachers()
  const { data: roomsData } = useRooms()
  const { data: sectionsData } = useSections()
  const courses: Course[] = coursesData?.data ?? []
  const teachers = teachersData?.data ?? []
  const rooms = roomsData?.data ?? []
  const sections = sectionsData?.data ?? []
  const { data: periodsData } = useQuery({
    queryKey: ["periods"],
    queryFn: () => periodsApi.list(),
  })
  const periods: Period[] = periodsData?.data ?? []
  const routineConflicts: RoutineConflict[] = useMemo(() => {
    if (conflictCount === 0) return []
    const conflictDetailIds = new Set<string>()
    const seen = new Map<string, string>()
    for (const d of details) {
      const key = `${d.day_of_week}-${d.start_time}-${d.room_code}`
      if (seen.has(key) && seen.get(key) !== d.teacher_name) {
        conflictDetailIds.add(d.id)
      }
      seen.set(key, d.teacher_name ?? "")
    }
    return [{
      type: "room" as const,
      description: `${conflictCount} conflict(s) detected`,
      detail_ids: Array.from(conflictDetailIds),
      severity: "error" as const,
    }]
  }, [conflictCount, details])

  if (loading) {
    return <div className="p-8 text-center text-muted-foreground">Loading routine...</div>
  }

  if (!routine) {
    return (
      <div className="space-y-6">
        <PageHeader title="Routine Not Found">
          <Link href="/routines"><Button variant="outline"><ArrowLeft className="mr-2 h-4 w-4" />Back</Button></Link>
        </PageHeader>
        <p className="text-muted-foreground">The requested routine could not be found.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <PageHeader title={routine.name ?? "Routine"}>
        <Link href="/routines">
          <Button variant="outline">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
        </Link>
      </PageHeader>

      <div className="flex flex-wrap items-center gap-4">
        <Badge variant={routine.status === "published" ? "default" : routine.status === "archived" ? "outline" : "secondary"}>
          {routine.status}
        </Badge>
        <span className="text-sm text-muted-foreground">
          {routine.session_name ?? ""} / {routine.batch_name ?? ""} / {routine.semester_name ?? ""}
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
        <Button size="sm" onClick={() => publishMutation.mutate(routineId)} disabled={routine.status === "published"}>
          <Play className="mr-2 h-4 w-4" />
          Publish
        </Button>
        <Button size="sm" variant="secondary" onClick={() => exportToPdf(details, routine.name ?? "Routine")}>
          <Download className="mr-2 h-4 w-4" />
          Export PDF
        </Button>
        <Button size="sm" variant="secondary" onClick={() => exportToExcel(details, routine.name ?? "Routine")}>
          <Download className="mr-2 h-4 w-4" />
          Export Excel
        </Button>
        <Button size="sm" variant="outline" onClick={() => cloneMutation.mutate(routineId, { onSuccess: (data) => router.push(`/routines/${data.id}`) })}>
          <Copy className="mr-2 h-4 w-4" />
          Clone
        </Button>
        <Button size="sm" variant="outline" onClick={() => archiveMutation.mutate(routineId)} disabled={routine.status === "archived"}>
          <Archive className="mr-2 h-4 w-4" />
          Archive
        </Button>
        <Button size="sm" variant="destructive" onClick={() => { if (confirm("Delete this routine?")) deleteMutation.mutate(routineId, { onSuccess: () => router.push("/routines") }) }}>
          <Trash2 className="mr-2 h-4 w-4" />
          Delete
        </Button>
      </div>

      <TimetableGrid
        details={details}
        periods={periods}
        onCellClick={handleCellClick}
        onCellEdit={handleCellEdit}
        onSlotMove={(detailId, targetDay, targetStartTime) => {
          updateDetailMutation.mutate({ day_of_week: targetDay, start_time: targetStartTime })
        }}
        conflicts={routineConflicts}
      />

      <SlotDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        onSave={handleSave}
        onDelete={editingId ? handleDelete : undefined}
        initialData={editingSlot}
        defaultDay={pendingDay}
        defaultStartTime={pendingTime}
        courses={courses.map((c) => ({ id: c.id, name: c.title, code: c.code }))}
        teachers={teachers.map((t: { id: string; display_name: string }) => ({ id: t.id, name: t.display_name }))}
        rooms={rooms.map((r: { id: string; name: string; code: string }) => ({ id: r.id, name: r.name, code: r.code }))}
        sections={sections.map((s: { id: string; name: string }) => ({ id: s.id, name: s.name }))}
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