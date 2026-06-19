"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { Role, Permission } from "@/types/roles"

interface RoleFormData {
  name: string
  description: string
  permission_ids: string[]
}

interface RoleDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: (data: RoleFormData) => void
  initialData?: Role | null
  permissions?: Permission[]
}

export function RoleDialog({ open, onOpenChange, onSave, initialData, permissions = [] }: RoleDialogProps) {
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [selectedPermissions, setSelectedPermissions] = useState<string[]>([])

  useEffect(() => {
    if (initialData) {
      setName(initialData.name)
      setDescription(initialData.description ?? "")
      setSelectedPermissions([])
    } else {
      setName("")
      setDescription("")
      setSelectedPermissions([])
    }
  }, [initialData, open])

  function togglePermission(permId: string) {
    setSelectedPermissions((prev) =>
      prev.includes(permId) ? prev.filter((id) => id !== permId) : [...prev, permId],
    )
  }

  const grouped = permissions.reduce<Record<string, Permission[]>>((acc, p) => {
    if (!acc[p.module]) acc[p.module] = []
    acc[p.module].push(p)
    return acc
  }, {})

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSave({ name, description, permission_ids: selectedPermissions })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Role" : "Add Role"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Role Name</Label>
            <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Department Admin" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Input id="description" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Manages department-level routines and courses" />
          </div>
          {permissions.length > 0 && (
            <div className="space-y-2">
              <Label>Permissions</Label>
              <div className="max-h-60 overflow-y-auto rounded-lg border p-3 space-y-3">
                {Object.entries(grouped).map(([module, perms]) => (
                  <div key={module}>
                    <p className="text-xs font-medium uppercase text-muted-foreground mb-1">{module}</p>
                    <div className="flex flex-wrap gap-2">
                      {perms.map((perm) => (
                        <label
                          key={perm.id}
                          className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1 text-xs cursor-pointer transition-colors ${
                            selectedPermissions.includes(perm.id)
                              ? "border-primary bg-primary/10 text-primary"
                              : "hover:bg-accent"
                          }`}
                        >
                          <input
                            type="checkbox"
                            checked={selectedPermissions.includes(perm.id)}
                            onChange={() => togglePermission(perm.id)}
                            className="sr-only"
                          />
                          {perm.name}
                        </label>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
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