"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { Teacher } from "@/types/teachers"

interface TeacherFormData {
  employee_id: string
  name: string
  email: string
  phone: string
  department: string
  specialization: string[]
  max_hours_per_week: number
  is_active: boolean
}

interface TeacherDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: TeacherFormData) => void
  initialData?: Teacher | null
}

export function TeacherDialog({ open, onOpenChange, onSave, initialData }: TeacherDialogProps) {
  const [employeeId, setEmployeeId] = useState("")
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [department, setDepartment] = useState("")
  const [specializationText, setSpecializationText] = useState("")
  const [maxHours, setMaxHours] = useState(20)

  useEffect(() => {
    if (initialData) {
      setEmployeeId(initialData.employee_id)
      setName(initialData.name)
      setEmail(initialData.email)
      setPhone(initialData.phone ?? "")
      setDepartment(initialData.department)
      setSpecializationText(initialData.specialization.join(", "))
      setMaxHours(initialData.max_hours_per_week)
    } else {
      setEmployeeId("")
      setName("")
      setEmail("")
      setPhone("")
      setDepartment("")
      setSpecializationText("")
      setMaxHours(20)
    }
  }, [initialData, open])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({
      employee_id: employeeId,
      name,
      email,
      phone,
      department,
      specialization: specializationText.split(",").map((s) => s.trim()).filter(Boolean),
      max_hours_per_week: maxHours,
      is_active: true,
    })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Teacher" : "Add Teacher"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="employeeId">Employee ID</Label>
              <Input id="employeeId" value={employeeId} onChange={(e) => setEmployeeId(e.target.value.toUpperCase())} placeholder="T-001" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="name">Full Name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Dr. Rahman" required />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="teacher@example.com" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone">Phone</Label>
              <Input id="phone" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="+8801XXXXXXXXX" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="department">Department</Label>
              <Input id="department" value={department} onChange={(e) => setDepartment(e.target.value)} placeholder="CSE" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="maxHours">Max Hours/Week</Label>
              <Input id="maxHours" type="number" value={maxHours} onChange={(e) => setMaxHours(Number(e.target.value))} min={1} max={60} />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="specialization">Specializations (comma-separated)</Label>
            <Input id="specialization" value={specializationText} onChange={(e) => setSpecializationText(e.target.value)} placeholder="Data Structures, Algorithms, DBMS" />
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
