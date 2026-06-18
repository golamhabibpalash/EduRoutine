"use client"

import { PageHeader } from "@/components/layout/page-header"
import { Clock } from "lucide-react"
import { Card } from "@/components/ui/card"

export function SchedulingPage() {
  return (
    <div>
      <PageHeader
        title="Scheduling Engine"
        description="Configure and run automatic timetable generation"
      />
      <Card className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <Clock className="h-12 w-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">Scheduling Engine</p>
        <p className="text-sm">Coming soon in Phase 2</p>
      </Card>
    </div>
  )
}

