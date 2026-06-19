"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { Semester } from "@/types/academic"

interface SemesterFormData {
  session_id: string
  name: string
  number: number
  start_date: string
  end_date: string
}

interface SemesterDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: SemesterFormData) => void
  initialData?: Semester | null
  sessions?: { id: string; name: string }[]
}

export function SemesterDialog({ open, onOpenChange, onSave, initialData, sessions = [] }: SemesterDialogProps) {
  const [sessionId, setSessionId] = useState("")
  const [name, setName] = useState("")
  const [number, setNumber] = useState(1)
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")

  useEffect(() => {
    if (initialData) {
      setSessionId(initialData.session_id)
      setName(initialData.name)
      setNumber(initialData.number)
      setStartDate(initialData.start_date.slice(0, 10))
      setEndDate(initialData.end_date.slice(0, 10))
    } else {
      setSessionId(sessions.length === 1 ? sessions[0].id : "")
      setName("")
      setNumber(1)
      setStartDate("")
      setEndDate("")
    }
  }, [initialData, open, sessions])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ session_id: sessionId, name, number, start_date: startDate, end_date: endDate })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Semester" : "Add Semester"}</DialogTitle>
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
              <Label htmlFor="number">Semester Number</Label>
              <Input id="number" type="number" value={number} onChange={(e) => setNumber(Number(e.target.value))} min={1} max={12} />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="name">Semester Name</Label>
            <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="1st Semester" required />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-2">
              <Label htmlFor="startDate">Start Date</Label>
              <Input id="startDate" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="endDate">End Date</Label>
              <Input id="endDate" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required />
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