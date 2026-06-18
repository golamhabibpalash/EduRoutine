"use client"

import { PageHeader } from "@/components/layout/page-header"
import { BarChart3 } from "lucide-react"
import { Card } from "@/components/ui/card"

export function ReportsPage() {
  return (
    <div>
      <PageHeader
        title="Reports & Analytics"
        description="View schedule reports and utilization analytics"
      />
      <Card className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <BarChart3 className="h-12 w-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">Reports & Analytics</p>
        <p className="text-sm">Coming soon in Phase 2</p>
      </Card>
    </div>
  )
}

