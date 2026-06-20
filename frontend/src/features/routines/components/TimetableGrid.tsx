"use client"

import { useState, useMemo, useCallback } from "react"
import type { RoutineDetail, DayOfWeek, Period, RoutineConflict } from "@/types/routines"

const DAYS: DayOfWeek[] = ["sunday", "monday", "tuesday", "wednesday", "thursday"]

const DAY_LABELS: Record<DayOfWeek, string> = {
  saturday: "Sat",
  sunday: "Sun",
  monday: "Mon",
  tuesday: "Tue",
  wednesday: "Wed",
  thursday: "Thu",
  friday: "Fri",
}

const PASTEL_COLORS = [
  "bg-blue-100 border-blue-300 text-blue-800",
  "bg-green-100 border-green-300 text-green-800",
  "bg-amber-100 border-amber-300 text-amber-800",
  "bg-rose-100 border-rose-300 text-rose-800",
  "bg-violet-100 border-violet-300 text-violet-800",
  "bg-cyan-100 border-cyan-300 text-cyan-800",
  "bg-orange-100 border-orange-300 text-orange-800",
  "bg-teal-100 border-teal-300 text-teal-800",
  "bg-pink-100 border-pink-300 text-pink-800",
  "bg-indigo-100 border-indigo-300 text-indigo-800",
]

interface SlotEntry {
  id: string
  courseCode: string
  courseName: string
  teacherName: string
  roomCode: string
  sectionName: string
  startTime: string
  endTime: string
  isLab: boolean
  colorIndex: number
}

interface TimetableGridProps {
  details: RoutineDetail[]
  periods?: Period[]
  onCellClick?: (day: DayOfWeek, startTime: string, endTime: string, periodId: string) => void
  onCellEdit?: (detailId: string) => void
  onSlotMove?: (detailId: string, targetDay: DayOfWeek, targetStartTime: string) => void
  conflicts?: RoutineConflict[]
  loading?: boolean
}

function hashColor(courseCode: string): number {
  let hash = 0
  for (let i = 0; i < courseCode.length; i++) {
    hash = courseCode.charCodeAt(i) + ((hash << 5) - hash)
  }
  return Math.abs(hash) % PASTEL_COLORS.length
}

function buildSlotsMap(details: RoutineDetail[]): Map<string, Map<string, SlotEntry>> {
  const map = new Map<string, Map<string, SlotEntry>>()
  for (const d of details) {
    const key = d.start_time
    if (!map.has(key)) map.set(key, new Map())
    const dayMap = map.get(key)!
    dayMap.set(d.day_of_week, {
      id: d.id,
      courseCode: d.course_code ?? "",
      courseName: d.course_name ?? "",
      teacherName: d.teacher_name ?? "",
      roomCode: d.room_code ?? "",
      sectionName: d.section_name ?? "",
      startTime: d.start_time,
      endTime: d.end_time,
      isLab: d.is_lab,
      colorIndex: hashColor(d.course_code ?? ""),
    })
  }
  return map
}

function getConflictIds(conflicts?: RoutineConflict[]): Set<string> {
  const ids = new Set<string>()
  if (!conflicts) return ids
  for (const c of conflicts) {
    for (const did of c.detail_ids) ids.add(did)
  }
  return ids
}

export function TimetableGrid({ details, periods, onCellClick, onCellEdit, onSlotMove, conflicts, loading }: TimetableGridProps) {
  const [dragOver, setDragOver] = useState<string | null>(null)
  const [dragSource, setDragSource] = useState<string | null>(null)

  const conflictIds = useMemo(() => getConflictIds(conflicts), [conflicts])

  const rows = useMemo(() => {
    const slotsMap = buildSlotsMap(details)

    if (periods && periods.length > 0) {
      return periods.map((p) => {
        const st = p.start_time.slice(0, 5)
        const dayMap = slotsMap.get(st) ?? new Map()
        const cells: Record<string, SlotEntry | null> = {}
        for (const day of DAYS) {
          cells[day] = dayMap.get(day) ?? null
        }
        return {
          label: `${p.name} (${st}-${p.end_time.slice(0, 5)})`,
          startTime: st,
          endTime: p.end_time.slice(0, 5),
          periodId: p.id,
          cells,
        }
      })
    }

    const timeSlots = new Map<string, { startTime: string; endTime: string; label: string }>()
    for (const d of details) {
      const key = d.start_time
      if (!timeSlots.has(key)) {
        timeSlots.set(key, {
          startTime: d.start_time,
          endTime: d.end_time,
          label: `${d.start_time.slice(0, 5)}-${d.end_time.slice(0, 5)}`,
        })
      }
    }

    return Array.from(timeSlots.keys()).sort().map((key) => {
      const slot = timeSlots.get(key)!
      const dayMap = slotsMap.get(key) ?? new Map()
      const cells: Record<string, SlotEntry | null> = {}
      for (const day of DAYS) {
        cells[day] = dayMap.get(day) ?? null
      }
      return { label: slot.label, startTime: slot.startTime, endTime: slot.endTime, periodId: "", cells }
    })
  }, [details, periods])

  const handleDragStart = useCallback((e: React.DragEvent, detailId: string) => {
    setDragSource(detailId)
    e.dataTransfer.effectAllowed = "move"
    e.dataTransfer.setData("text/plain", detailId)
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent, cellKey: string) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = "move"
    setDragOver(cellKey)
  }, [])

  const handleDragLeave = useCallback(() => {
    setDragOver(null)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent, targetDay: DayOfWeek, targetStartTime: string) => {
    e.preventDefault()
    setDragOver(null)
    const detailId = e.dataTransfer.getData("text/plain")
    if (detailId && onSlotMove) {
      onSlotMove(detailId, targetDay, targetStartTime)
    }
    setDragSource(null)
  }, [onSlotMove])

  function makeCellKey(day: string, time: string) {
    return `${day}-${time}`
  }

  if (loading) {
    return (
      <div className="rounded-md border p-12 text-center text-muted-foreground">
        Loading timetable...
      </div>
    )
  }

  if (rows.length === 0) {
    return (
      <div className="rounded-md border p-12 text-center text-muted-foreground">
        No schedule entries yet. Click a cell to add a class.
      </div>
    )
  }

  return (
    <div className="overflow-x-auto rounded-md border">
      <table className="w-full min-w-[640px] border-collapse text-sm">
        <thead>
          <tr>
            <th className="border-b border-r bg-muted/50 px-3 py-2 text-left text-xs font-medium text-muted-foreground w-32">
              Period
            </th>
            {DAYS.map((day) => (
              <th
                key={day}
                className="border-b border-r bg-muted/50 px-3 py-2 text-center text-xs font-medium text-muted-foreground"
              >
                {DAY_LABELS[day]}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.startTime}>
              <td className="border-b border-r px-3 py-2 text-xs text-muted-foreground whitespace-nowrap align-top">
                {row.label}
              </td>
              {DAYS.map((day) => {
                const entry = row.cells[day]
                const ck = makeCellKey(day, row.startTime)
                const isOver = dragOver === ck
                const hasConflict = entry && conflictIds.has(entry.id)

                return (
                  <td
                    key={day}
                    className={`border-b border-r p-1 align-top transition-colors ${
                      isOver ? "bg-accent/40" : ""
                    } ${entry && !isOver ? "" : ""}`}
                    onDragOver={(e) => handleDragOver(e, ck)}
                    onDragLeave={handleDragLeave}
                    onDrop={(e) => handleDrop(e, day, row.startTime)}
                    onClick={() => {
                      if (entry && onCellEdit) {
                        onCellEdit(entry.id)
                      }
                      if (!entry && onCellClick) {
                        onCellClick(day, row.startTime, row.endTime, row.periodId)
                      }
                    }}
                  >
                    {entry ? (
                      <div
                        draggable={!!onSlotMove}
                        onDragStart={(e) => handleDragStart(e, entry.id)}
                        className={`rounded border px-1.5 py-1 text-xs cursor-${onSlotMove ? "grab" : "pointer"} ${
                          PASTEL_COLORS[entry.colorIndex]
                        } ${hasConflict ? "ring-2 ring-destructive" : ""} ${
                          dragSource === entry.id ? "opacity-40" : ""
                        }`}
                      >
                        <div className="font-medium truncate">{entry.courseCode}</div>
                        <div className="truncate opacity-75">{entry.teacherName}</div>
                        <div className="truncate opacity-60">{entry.roomCode}</div>
                        {entry.isLab && (
                          <span className="mt-0.5 inline-block rounded bg-black/10 px-1 text-[10px]">
                            Lab
                          </span>
                        )}
                      </div>
                    ) : (
                      <div
                        className={`min-h-[48px] rounded border border-dashed cursor-pointer transition-colors ${
                          isOver
                            ? "border-primary bg-primary/10"
                            : "border-muted-300 hover:bg-accent/30"
                        }`}
                        onClick={() => onCellClick?.(day, row.startTime, row.endTime, row.periodId)}
                      />
                    )}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}