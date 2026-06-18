"use client"

import { PageHeader } from "@/components/layout/page-header"
import { Calendar } from "lucide-react"
import { Card } from "@/components/ui/card"

export function RoutinesPage() {
  return (
    <div>
      <PageHeader
        title="Routine Management"
        description="Manage academic timetables and class schedules"
      />
      <Card className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <Calendar className="h-12 w-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">Routine Management</p>
        <p className="text-sm">Coming soon in Phase 2</p>
      </Card>
    </div>
  )
}

