"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { Section } from "@/types/academic"

interface SectionFormData {
  batch_id: string
  name: string
  max_capacity: number
}

interface SectionDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: SectionFormData) => void
  initialData?: Section | null
  batches?: { id: string; name: string; code: string }[]
}

export function SectionDialog({ open, onOpenChange, onSave, initialData, batches = [] }: SectionDialogProps) {
  const [batchId, setBatchId] = useState("")
  const [name, setName] = useState("")
  const [maxCapacity, setMaxCapacity] = useState(60)

  useEffect(() => {
    if (initialData) {
      setBatchId(initialData.batch_id)
      setName(initialData.name)
      setMaxCapacity(initialData.max_capacity)
    } else {
      setBatchId(batches.length === 1 ? batches[0].id : "")
      setName("")
      setMaxCapacity(60)
    }
  }, [initialData, open, batches])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ batch_id: batchId, name, max_capacity: maxCapacity })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-sm">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Section" : "Add Section"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="batchId">Batch</Label>
            <select id="batchId" value={batchId} onChange={(e) => setBatchId(e.target.value)} required
              className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm">
              <option value="">Select batch...</option>
              {batches.map((b) => <option key={b.id} value={b.id}>{b.name} ({b.code})</option>)}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-2">
              <Label htmlFor="name">Section Name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="A" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="maxCapacity">Max Capacity</Label>
              <Input id="maxCapacity" type="number" value={maxCapacity} onChange={(e) => setMaxCapacity(Number(e.target.value))} min={1} max={500} />
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