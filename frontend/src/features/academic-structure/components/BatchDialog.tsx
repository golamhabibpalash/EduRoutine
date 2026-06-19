"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { Batch } from "@/types/academic"

interface BatchFormData {
  session_id: string
  department_id: string
  name: string
  code: string
}

interface BatchDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: BatchFormData) => void
  initialData?: Batch | null
  departments?: { id: string; name: string; code: string }[]
  sessions?: { id: string; name: string }[]
}

export function BatchDialog({ open, onOpenChange, onSave, initialData, departments = [], sessions = [] }: BatchDialogProps) {
  const [sessionId, setSessionId] = useState("")
  const [departmentId, setDepartmentId] = useState("")
  const [name, setName] = useState("")
  const [code, setCode] = useState("")

  useEffect(() => {
    if (initialData) {
      setSessionId(initialData.session_id)
      setDepartmentId(initialData.department_id)
      setName(initialData.name)
      setCode(initialData.code)
    } else {
      setSessionId(sessions.length === 1 ? sessions[0].id : "")
      setDepartmentId(departments.length === 1 ? departments[0].id : "")
      setName("")
      setCode("")
    }
  }, [initialData, open, departments, sessions])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ session_id: sessionId, department_id: departmentId, name, code })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Batch" : "Add Batch"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-2">
              <Label htmlFor="sessionId">Session</Label>
              <select id="sessionId" value={sessionId} onChange={(e) => setSessionId(e.target.value)} required
                className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm">
                <option value="">Select session...</option>
                {sessions.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
              </select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="departmentId">Department</Label>
              <select id="departmentId" value={departmentId} onChange={(e) => setDepartmentId(e.target.value)} required
                className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm">
                <option value="">Select department...</option>
                {departments.map((d) => <option key={d.id} value={d.id}>{d.name} ({d.code})</option>)}
              </select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-2">
              <Label htmlFor="name">Batch Name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Batch 1" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="code">Batch Code</Label>
              <Input id="code" value={code} onChange={(e) => setCode(e.target.value.toUpperCase().slice(0, 20))} placeholder="B1-CSE-2026" required />
            </div>
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