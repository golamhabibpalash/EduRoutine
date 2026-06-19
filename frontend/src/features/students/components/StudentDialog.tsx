"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { Student } from "@/types/students"

interface StudentFormData {
  student_id: string
  name: string
  email: string
  phone: string
  batch_id: string
  section_id: string
  enrollment_year: number
  is_active: boolean
}

interface StudentDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: StudentFormData) => void
  initialData?: Student | null
}

export function StudentDialog({ open, onOpenChange, onSave, initialData }: StudentDialogProps) {
  const [studentId, setStudentId] = useState("")
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [batchId, setBatchId] = useState("")
  const [sectionId, setSectionId] = useState("")
  const [enrollmentYear, setEnrollmentYear] = useState(new Date().getFullYear())

  useEffect(() => {
    if (initialData) {
      setStudentId(initialData.student_id)
      setName(initialData.name)
      setEmail(initialData.email)
      setPhone(initialData.phone ?? "")
      setBatchId(initialData.batch_id)
      setSectionId(initialData.section_id)
      setEnrollmentYear(initialData.enrollment_year)
    } else {
      setStudentId("")
      setName("")
      setEmail("")
      setPhone("")
      setBatchId("")
      setSectionId("")
      setEnrollmentYear(new Date().getFullYear())
    }
  }, [initialData, open])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ student_id: studentId, name, email, phone, batch_id: batchId, section_id: sectionId, enrollment_year: enrollmentYear, is_active: true })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Student" : "Add Student"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="studentId">Student ID</Label>
              <Input id="studentId" value={studentId} onChange={(e) => setStudentId(e.target.value.toUpperCase())} placeholder="CSE-48-001" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="name">Full Name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="John Doe" required />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="john@example.com" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone">Phone</Label>
              <Input id="phone" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="+8801XXXXXXXXX" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="batch">Batch ID</Label>
              <Input id="batch" value={batchId} onChange={(e) => setBatchId(e.target.value)} placeholder="batch-id" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="section">Section ID</Label>
              <Input id="section" value={sectionId} onChange={(e) => setSectionId(e.target.value)} placeholder="section-id" />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="enrollmentYear">Enrollment Year</Label>
            <Input id="enrollmentYear" type="number" value={enrollmentYear} onChange={(e) => setEnrollmentYear(Number(e.target.value))} min={2000} max={2100} />
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
