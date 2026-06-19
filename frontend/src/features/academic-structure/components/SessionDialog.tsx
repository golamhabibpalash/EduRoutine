"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { Session } from "@/types/academic"

interface SessionFormData {
  name: string
  start_date: string
  end_date: string
  is_current: boolean
}

interface SessionDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: SessionFormData) => void
  initialData?: Session | null
}

export function SessionDialog({ open, onOpenChange, onSave, initialData }: SessionDialogProps) {
  const [name, setName] = useState("")
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")
  const [isCurrent, setIsCurrent] = useState(false)

  useEffect(() => {
    if (initialData) {
      setName(initialData.name)
      setStartDate(initialData.start_date.slice(0, 10))
      setEndDate(initialData.end_date.slice(0, 10))
      setIsCurrent(initialData.is_current)
    } else {
      setName("")
      setStartDate("")
      setEndDate("")
      setIsCurrent(false)
    }
  }, [initialData, open])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ name, start_date: startDate, end_date: endDate, is_current: isCurrent })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-sm">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Session" : "Add Session"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Session Name</Label>
            <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="2026-2027" required />
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
          {!initialData && (
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={isCurrent} onChange={(e) => setIsCurrent(e.target.checked)} className="rounded" />
              Set as current session
            </label>
          )}
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
            <Button type="submit">{initialData ? "Update" : "Create"}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}