"use client"

import { PageHeader } from "@/components/layout/page-header"
import { DoorOpen } from "lucide-react"
import { Card } from "@/components/ui/card"

export function RoomsPage() {
  return (
    <div>
      <PageHeader
        title="Room Inventory"
        description="Manage classrooms, labs, and facilities"
      />
      <Card className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <DoorOpen className="h-12 w-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">Room Inventory</p>
        <p className="text-sm">Coming soon in Phase 2</p>
      </Card>
    </div>
  )
}

