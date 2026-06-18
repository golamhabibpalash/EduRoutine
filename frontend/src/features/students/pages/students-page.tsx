"use client"

import { PageHeader } from "@/components/layout/page-header"
import { GraduationCap } from "lucide-react"
import { Card } from "@/components/ui/card"

export function StudentsPage() {
  return (
    <div>
      <PageHeader
        title="Student Records"
        description="View and manage student enrollments"
      />
      <Card className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <GraduationCap className="h-12 w-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">Student Records</p>
        <p className="text-sm">Coming soon in Phase 2</p>
      </Card>
    </div>
  )
}

