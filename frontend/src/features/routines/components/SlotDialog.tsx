"use client"

import { useState, useEffect, useRef } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import type { DayOfWeek } from "@/types/routines"

interface SelectOption {
  id: string
  name: string
  code?: string
}

export interface SlotFormData {
  course_id: string
  course_code: string
  course_name: string
  teacher_id: string
  teacher_name: string
  room_id: string
  room_code: string
  section_id: string
  section_name: string
  startTime: string
  endTime: string
  isLab: boolean
}

interface SlotDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: SlotFormData) => void
  onDelete?: () => void
  initialData?: SlotFormData | null
  defaultDay?: DayOfWeek | null
  defaultStartTime?: string | null
  defaultEndTime?: string | null
  periodDurationMinutes?: number
  courses?: SelectOption[]
  teachers?: SelectOption[]
  rooms?: SelectOption[]
  sections?: SelectOption[]
}

function SelectField({ label, options, value, onChange }: { label: string; options: SelectOption[]; value: string; onChange: (v: string) => void }) {
  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required
        className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
      >
        <option value="">Select {label.toLowerCase()}...</option>
        {options.map((o) => (
          <option key={o.id} value={o.id}>{o.code ? `${o.name} (${o.code})` : o.name}</option>
        ))}
      </select>
    </div>
  )
}

function addMinutes(time: string, mins: number) {
  const [h, m] = time.split(":").map(Number)
  const d = new Date(2020, 0, 1, h, m + mins)
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`
}

function SearchableRoomField({ label, options, value, onChange }: { label: string; options: SelectOption[]; value: string; onChange: (v: string) => void }) {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState("")
  const containerRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const selected = options.find((o) => o.id === value)

  const filtered = options.filter(
    (o) => !query || o.name.toLowerCase().includes(query.toLowerCase()) || (o.code ?? "").toLowerCase().includes(query.toLowerCase())
  )

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  return (
    <div className="space-y-2" ref={containerRef}>
      <Label>{label}</Label>
      <div className="relative">
        <input
          ref={inputRef}
          value={open ? query : selected ? `${selected.name}${selected.code ? ` (${selected.code})` : ""}` : ""}
          onChange={(e) => { setQuery(e.target.value); setOpen(true) }}
          onFocus={() => { setOpen(true); setQuery("") }}
          placeholder={`Search ${label.toLowerCase()}...`}
          className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm outline-none focus-visible:ring-1 focus-visible:ring-ring"
        />
        {open && (
          <div className="absolute z-10 mt-1 max-h-48 w-full overflow-auto rounded-md border bg-popover p-1 shadow-md">
            {filtered.length === 0 ? (
              <div className="px-2 py-1 text-sm text-muted-foreground">No results</div>
            ) : (
              filtered.map((o) => (
                <button
                  key={o.id}
                  type="button"
                  className={`flex w-full items-center rounded-sm px-2 py-1.5 text-sm text-left hover:bg-accent hover:text-accent-foreground ${o.id === value ? "bg-accent" : ""}`}
                  onClick={() => { onChange(o.id); setOpen(false); setQuery("") }}
                >
                  {o.name}{o.code ? ` (${o.code})` : ""}
                </button>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export function SlotDialog({
  open,
  onOpenChange,
  onSave,
  onDelete,
  initialData,
  defaultDay,
  defaultStartTime,
  defaultEndTime,
  periodDurationMinutes = 50,
  courses = [],
  teachers = [],
  rooms = [],
  sections = [],
}: SlotDialogProps) {
  const [courseId, setCourseId] = useState("")
  const [teacherId, setTeacherId] = useState("")
  const [roomId, setRoomId] = useState("")
  const [sectionId, setSectionId] = useState("")
  const [startTime, setStartTime] = useState("")
  const [endTime, setEndTime] = useState("")
  const [isLab, setIsLab] = useState(false)

  useEffect(() => {
    if (initialData) {
      setCourseId(initialData.course_id)
      setTeacherId(initialData.teacher_id)
      setRoomId(initialData.room_id)
      setSectionId(initialData.section_id)
      setStartTime(initialData.startTime)
      setEndTime(initialData.endTime)
      setIsLab(initialData.isLab)
    } else {
      setCourseId("")
      setTeacherId("")
      setRoomId("")
      setSectionId("")
      const st = defaultStartTime ?? "08:00"
      setStartTime(st)
      setEndTime(defaultEndTime ?? addMinutes(st, periodDurationMinutes))
      setIsLab(false)
    }
  }, [initialData, defaultStartTime, defaultEndTime, periodDurationMinutes, open])

  function lookup(id: string, items: SelectOption[]) {
    return items.find((o) => o.id === id)
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const course = lookup(courseId, courses)
    const teacher = lookup(teacherId, teachers)
    const room = lookup(roomId, rooms)
    const section = lookup(sectionId, sections)
    onSave({
      course_id: courseId,
      course_code: course?.code ?? "",
      course_name: course?.name ?? "",
      teacher_id: teacherId,
      teacher_name: teacher?.name ?? "",
      room_id: roomId,
      room_code: room?.code ?? "",
      section_id: sectionId,
      section_name: section?.name ?? "",
      startTime,
      endTime,
      isLab,
    })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Slot" : "Add Slot"}</DialogTitle>
          <DialogDescription>
            {initialData ? "Update the class entry for this time slot." : "Assign a course to this time slot."}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <SelectField label="Course" options={courses} value={courseId} onChange={setCourseId} />
            <SelectField label="Teacher" options={teachers} value={teacherId} onChange={setTeacherId} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <SearchableRoomField label="Room" options={rooms} value={roomId} onChange={setRoomId} />
            <SelectField label="Section" options={sections} value={sectionId} onChange={setSectionId} />
          </div>
          <div className="flex items-center gap-2">
            <input type="checkbox" id="isLab" checked={isLab} onChange={(e) => setIsLab(e.target.checked)} className="h-4 w-4 rounded border-gray-300" />
            <Label htmlFor="isLab">Lab Session</Label>
          </div>
          <DialogFooter className="gap-2">
            {onDelete && initialData && (
              <Button type="button" variant="destructive" onClick={onDelete} className="mr-auto">
                Remove
              </Button>
            )}
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit">{initialData ? "Update" : "Add"}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}