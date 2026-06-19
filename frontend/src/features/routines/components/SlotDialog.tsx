"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { DayOfWeek } from "@/types/routines"

const DAY_OPTIONS: { value: DayOfWeek; label: string }[] = [
  { value: "sunday", label: "Sunday" },
  { value: "monday", label: "Monday" },
  { value: "tuesday", label: "Tuesday" },
  { value: "wednesday", label: "Wednesday" },
  { value: "thursday", label: "Thursday" },
]

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

interface SlotDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: SlotFormData) => void
  onDelete?: () => void
  initialData?: SlotFormData | null
  defaultDay?: DayOfWeek | null
  defaultStartTime?: string | null
}

export function SlotDialog({
  open,
  onOpenChange,
  onSave,
  onDelete,
  initialData,
  defaultDay,
  defaultStartTime,
}: SlotDialogProps) {
  const [courseCode, setCourseCode] = useState("")
  const [courseName, setCourseName] = useState("")
  const [teacherName, setTeacherName] = useState("")
  const [roomCode, setRoomCode] = useState("")
  const [sectionName, setSectionName] = useState("")
  const [startTime, setStartTime] = useState("")
  const [endTime, setEndTime] = useState("")
  const [isLab, setIsLab] = useState(false)

  useEffect(() => {
    if (initialData) {
      setCourseCode(initialData.courseCode)
      setCourseName(initialData.courseName)
      setTeacherName(initialData.teacherName)
      setRoomCode(initialData.roomCode)
      setSectionName(initialData.sectionName)
      setStartTime(initialData.startTime)
      setEndTime(initialData.endTime)
      setIsLab(initialData.isLab)
    } else {
      setCourseCode("")
      setCourseName("")
      setTeacherName("")
      setRoomCode("")
      setSectionName("")
      setStartTime(defaultStartTime ?? "08:00")
      setEndTime("")
      setIsLab(false)
    }
  }, [initialData, defaultStartTime, open])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ courseCode, courseName, teacherName, roomCode, sectionName, startTime, endTime, isLab })
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
            <div className="space-y-2">
              <Label htmlFor="courseCode">Course Code</Label>
              <Input id="courseCode" value={courseCode} onChange={(e) => setCourseCode(e.target.value.toUpperCase())} placeholder="CSE-101" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="courseName">Course Name</Label>
              <Input id="courseName" value={courseName} onChange={(e) => setCourseName(e.target.value)} placeholder="Data Structures" required />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="teacherName">Teacher</Label>
              <Input id="teacherName" value={teacherName} onChange={(e) => setTeacherName(e.target.value)} placeholder="Dr. Rahman" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="roomCode">Room</Label>
              <Input id="roomCode" value={roomCode} onChange={(e) => setRoomCode(e.target.value.toUpperCase())} placeholder="301" required />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="sectionName">Section</Label>
              <Input id="sectionName" value={sectionName} onChange={(e) => setSectionName(e.target.value)} placeholder="A" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="startTime">Start Time</Label>
              <Input id="startTime" type="time" value={startTime} onChange={(e) => setStartTime(e.target.value)} required />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="endTime">End Time</Label>
              <Input id="endTime" type="time" value={endTime} onChange={(e) => setEndTime(e.target.value)} required />
            </div>
            <div className="flex items-end pb-2">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" checked={isLab} onChange={(e) => setIsLab(e.target.checked)} className="h-4 w-4 rounded border-gray-300" />
                <span className="text-sm">Lab Session</span>
              </label>
            </div>
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
