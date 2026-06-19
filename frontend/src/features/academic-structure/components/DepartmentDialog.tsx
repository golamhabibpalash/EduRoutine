"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { Department } from "@/types/academic"

interface DepartmentFormData {
  name: string
  code: string
}

interface DepartmentDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: DepartmentFormData) => void
  initialData?: Department | null
}

export function DepartmentDialog({ open, onOpenChange, onSave, initialData }: DepartmentDialogProps) {
  const [name, setName] = useState("")
  const [code, setCode] = useState("")

  useEffect(() => {
    if (initialData) {
      setName(initialData.name)
      setCode(initialData.code)
    } else {
      setName("")
      setCode("")
    }
  }, [initialData, open])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ name, code })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-sm">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Department" : "Add Department"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Department Name</Label>
            <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Computer Science & Engineering" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="code">Department Code</Label>
            <Input id="code" value={code} onChange={(e) => setCode(e.target.value.toUpperCase().slice(0, 10))} placeholder="CSE" required />
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