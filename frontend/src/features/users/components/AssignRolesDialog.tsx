"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { useRoles } from "@/hooks/use-roles"
import { useAssignRoles } from "@/hooks/use-users"
import type { User } from "@/types/users"

interface AssignRolesDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  user: User
}

export function AssignRolesDialog({ open, onOpenChange, user }: AssignRolesDialogProps) {
  const { data: rolesData } = useRoles()
  const assignMutation = useAssignRoles()
  const [selectedIds, setSelectedIds] = useState<string[]>([])

  const roles = rolesData?.data ?? []

  useEffect(() => {
    if (open) setSelectedIds(user.roles)
  }, [open, user.roles])

  function toggleRole(roleId: string) {
    setSelectedIds((prev) =>
      prev.includes(roleId) ? prev.filter((id) => id !== roleId) : [...prev, roleId],
    )
  }

  function handleSave() {
    assignMutation.mutate(
      { userId: user.id, roleIds: selectedIds },
      { onSuccess: () => onOpenChange(false) },
    )
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-sm">
        <DialogHeader>
          <DialogTitle>Manage Roles — {user.display_name || user.email}</DialogTitle>
        </DialogHeader>
        <div className="space-y-3 py-2">
          {roles.length === 0 && <p className="text-sm text-muted-foreground">Loading roles...</p>}
          {roles.map((r: { id: string; name: string; description: string | null }) => (
            <label key={r.id} className={`flex items-center gap-3 rounded-lg border p-3 cursor-pointer transition-colors ${selectedIds.includes(r.id) ? "border-primary bg-primary/5" : "hover:bg-accent"}`}>
              <input
                type="checkbox"
                checked={selectedIds.includes(r.id)}
                onChange={() => toggleRole(r.id)}
                className="h-4 w-4 rounded border-gray-300 text-primary"
              />
              <div>
                <div className="text-sm font-medium">{r.name}</div>
                {r.description && <div className="text-xs text-muted-foreground">{r.description}</div>}
              </div>
            </label>
          ))}
        </div>
        <DialogFooter>
          <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
          <Button type="button" onClick={handleSave} disabled={assignMutation.isPending}>
            {assignMutation.isPending ? "Saving..." : "Save"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}