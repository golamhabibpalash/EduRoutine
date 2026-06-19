"use client"

import { useState, useEffect, useRef } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { X, Plus } from "lucide-react"
import type { Teacher } from "@/types/teachers"
import type { Department, Course } from "@/types/academic"

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
  departments: Department[]
  courses: Course[]
}

export function TeacherDialog({ open, onOpenChange, onSave, initialData, departments, courses }: TeacherDialogProps) {
  const [employeeId, setEmployeeId] = useState("")
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [department, setDepartment] = useState("")
  const [specializations, setSpecializations] = useState<string[]>([])
  const [maxHours, setMaxHours] = useState(20)

  const [pendingSpecialization, setPendingSpecialization] = useState("")
  const pendingRef = useRef<HTMLInputElement>(null)

  const courseNames = courses.map((c) => c.title)

  useEffect(() => {
    if (initialData) {
      setEmployeeId(initialData.employee_id)
      setName(initialData.name)
      setEmail(initialData.email)
      setPhone(initialData.phone ?? "")
      setDepartment(initialData.department)
      setSpecializations(initialData.specialization)
      setMaxHours(initialData.max_hours_per_week)
    } else {
      setEmployeeId("")
      setName("")
      setEmail("")
      setPhone("")
      setDepartment(departments.length > 0 ? departments[0].name : "")
      setSpecializations([])
      setMaxHours(20)
    }
  }, [initialData, open, departments])

  function addSpecialization(raw: string) {
    const val = raw.trim()
    if (val && !specializations.includes(val)) {
      setSpecializations([...specializations, val])
    }
  }

  function removeSpecialization(val: string) {
    setSpecializations(specializations.filter((s) => s !== val))
  }

  function handleSpecializationKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      e.preventDefault()
      addSpecialization(pendingSpecialization)
      setPendingSpecialization("")
      pendingRef.current?.focus()
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({
      employee_id: employeeId,
      name,
      email,
      phone,
      department,
      specialization: specializations,
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
              <Select value={department} onValueChange={(v) => setDepartment(v as string)} required>
                <SelectTrigger id="department">
                  <SelectValue placeholder="Select a department" />
                </SelectTrigger>
                <SelectContent>
                  {departments.map((dept) => (
                    <SelectItem key={dept.id} value={dept.name}>{dept.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="maxHours">Max Hours/Week</Label>
              <Input id="maxHours" type="number" value={maxHours} onChange={(e) => setMaxHours(Number(e.target.value))} min={1} max={60} />
            </div>
          </div>
          <div className="space-y-2">
            <Label>Specializations</Label>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Input
                  ref={pendingRef}
                  value={pendingSpecialization}
                  onChange={(e) => setPendingSpecialization(e.target.value)}
                  onKeyDown={handleSpecializationKeyDown}
                  placeholder="Type or choose from courses..."
                  list="course-suggestions"
                />
                <datalist id="course-suggestions">
                  {courseNames
                    .filter((name) => !specializations.includes(name))
                    .map((name) => (
                      <option key={name} value={name} />
                    ))}
                </datalist>
              </div>
              <Button type="button" size="icon" variant="outline" onClick={() => { addSpecialization(pendingSpecialization); setPendingSpecialization(""); pendingRef.current?.focus() }}>
                <Plus className="h-4 w-4" />
              </Button>
            </div>
            {specializations.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mt-2">
                {specializations.map((s) => (
                  <Badge key={s} variant="secondary" className="gap-1">
                    {s}
                    <button type="button" onClick={() => removeSpecialization(s)} className="ml-0.5 hover:text-destructive">
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ))}
              </div>
            )}
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
