"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import type { Course, Department } from "@/types/academic"

interface CourseFormData {
  department_id: string
  code: string
  title: string
  credits: number
  lecture_hours: number
  lab_hours: number
  is_active?: boolean
  prerequisite_ids?: string[]
}

interface CourseDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: CourseFormData) => void
  initialData?: Course | null
  departments: Department[]
}

export function CourseDialog({ open, onOpenChange, onSave, initialData, departments }: CourseDialogProps) {
  const [departmentId, setDepartmentId] = useState("")
  const [code, setCode] = useState("")
  const [title, setTitle] = useState("")
  const [credits, setCredits] = useState(3)
  const [lectureHours, setLectureHours] = useState(3)
  const [labHours, setLabHours] = useState(0)
  const [isActive, setIsActive] = useState(true)

  useEffect(() => {
    if (initialData) {
      setDepartmentId(initialData.department_id)
      setCode(initialData.code)
      setTitle(initialData.title)
      setCredits(initialData.credits)
      setLectureHours(initialData.lecture_hours)
      setLabHours(initialData.lab_hours)
      setIsActive(initialData.is_active)
    } else {
      setDepartmentId("")
      setCode("")
      setTitle("")
      setCredits(3)
      setLectureHours(3)
      setLabHours(0)
      setIsActive(true)
    }
  }, [initialData, open])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ department_id: departmentId, code, title, credits, lecture_hours: lectureHours, lab_hours: labHours, is_active: isActive })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Course" : "Add Course"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="code">Course Code</Label>
              <Input id="code" value={code} onChange={(e) => setCode(e.target.value.toUpperCase())} placeholder="CSE-101" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="title">Course Title</Label>
              <Input id="title" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Data Structures" required />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="departmentId">Department</Label>
            <Select value={departmentId} onValueChange={(v) => setDepartmentId(v as string)} required>
              <SelectTrigger id="departmentId">
                <SelectValue placeholder="Select a department" />
              </SelectTrigger>
              <SelectContent>
                {departments.map((dept) => (
                  <SelectItem key={dept.id} value={dept.id}>{dept.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-3 gap-3">
            <div className="space-y-2">
              <Label htmlFor="credits">Credits</Label>
              <Input id="credits" type="number" value={credits} onChange={(e) => setCredits(Number(e.target.value))} min={1} max={6} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="lectureHours">Lecture Hours</Label>
              <Input id="lectureHours" type="number" value={lectureHours} onChange={(e) => setLectureHours(Number(e.target.value))} min={0} max={6} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="labHours">Lab Hours</Label>
              <Input id="labHours" type="number" value={labHours} onChange={(e) => setLabHours(Number(e.target.value))} min={0} max={6} />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Checkbox id="isActive" checked={isActive} onCheckedChange={(c) => setIsActive(c === true)} />
            <Label htmlFor="isActive">Active</Label>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
            <Button type="submit">{initialData ? "Update" : "Create"}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
