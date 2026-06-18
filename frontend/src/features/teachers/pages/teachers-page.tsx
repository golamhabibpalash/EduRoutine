"use client"

import { PageHeader } from "@/components/layout/page-header"
import { UserCircle } from "lucide-react"
import { Card } from "@/components/ui/card"

export function TeachersPage() {
  return (
    <div>
      <PageHeader
        title="Teacher Directory"
        description="Manage faculty and instructor profiles"
      />
      <Card className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <UserCircle className="h-12 w-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">Teacher Directory</p>
        <p className="text-sm">Coming soon in Phase 2</p>
      </Card>
    </div>
  )
}

