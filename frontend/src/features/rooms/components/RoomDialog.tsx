"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { Room, RoomType } from "@/types/rooms"

const ROOM_TYPES: { value: RoomType; label: string }[] = [
  { value: "classroom", label: "Classroom" },
  { value: "lab", label: "Lab" },
  { value: "lecture_hall", label: "Lecture Hall" },
  { value: "seminar_room", label: "Seminar Room" },
  { value: "conference_room", label: "Conference Room" },
]

interface RoomFormData {
  code: string
  name: string
  type: RoomType
  capacity: number
  building: string
  floor: number
  has_projector: boolean
  has_computers: boolean
  has_ac: boolean
  is_active: boolean
}

interface RoomDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: RoomFormData) => void
  initialData?: Room | null
}

export function RoomDialog({ open, onOpenChange, onSave, initialData }: RoomDialogProps) {
  const [code, setCode] = useState("")
  const [name, setName] = useState("")
  const [type, setType] = useState<RoomType>("classroom")
  const [capacity, setCapacity] = useState(40)
  const [building, setBuilding] = useState("")
  const [floor, setFloor] = useState(1)
  const [hasProjector, setHasProjector] = useState(false)
  const [hasComputers, setHasComputers] = useState(false)
  const [hasAc, setHasAc] = useState(false)

  useEffect(() => {
    if (initialData) {
      setCode(initialData.code)
      setName(initialData.name)
      setType(initialData.type)
      setCapacity(initialData.capacity)
      setBuilding(initialData.building)
      setFloor(initialData.floor)
      setHasProjector(initialData.has_projector)
      setHasComputers(initialData.has_computers)
      setHasAc(initialData.has_ac)
    } else {
      setCode("")
      setName("")
      setType("classroom")
      setCapacity(40)
      setBuilding("")
      setFloor(1)
      setHasProjector(false)
      setHasComputers(false)
      setHasAc(false)
    }
  }, [initialData, open])

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ code, name, type, capacity, building, floor, has_projector: hasProjector, has_computers: hasComputers, has_ac: hasAc, is_active: true })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Room" : "Add Room"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="code">Room Code</Label>
              <Input id="code" value={code} onChange={(e) => setCode(e.target.value.toUpperCase())} placeholder="301" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="name">Room Name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Room 301" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="type">Type</Label>
              <select id="type" value={type} onChange={(e) => setType(e.target.value as RoomType)} className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                {ROOM_TYPES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
              </select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="capacity">Capacity</Label>
              <Input id="capacity" type="number" value={capacity} onChange={(e) => setCapacity(Number(e.target.value))} min={1} max={500} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="building">Building</Label>
              <Input id="building" value={building} onChange={(e) => setBuilding(e.target.value)} placeholder="Main Building" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="floor">Floor</Label>
              <Input id="floor" type="number" value={floor} onChange={(e) => setFloor(Number(e.target.value))} min={0} max={50} />
            </div>
          </div>
          <div className="flex flex-wrap gap-6">
            {[
              ["hasProjector", "Projector", hasProjector, setHasProjector],
              ["hasComputers", "Computers", hasComputers, setHasComputers],
              ["hasAc", "Air Conditioning", hasAc, setHasAc],
            ].map(([_, label, checked, setter]) => (
              <label key={_ as string} className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" checked={checked as boolean} onChange={() => (setter as (v: boolean) => void)(!(checked as boolean))} className="h-4 w-4 rounded border-gray-300" />
                <span className="text-sm">{label as string}</span>
              </label>
            ))}
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
