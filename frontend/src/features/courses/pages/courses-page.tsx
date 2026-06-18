"use client"

import { PageHeader } from "@/components/layout/page-header"
import { BookOpen } from "lucide-react"
import { Card } from "@/components/ui/card"

export function CoursesPage() {
  return (
    <div>
      <PageHeader
        title="Course Catalog"
        description="Create and manage course offerings"
      />
      <Card className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <BookOpen className="h-12 w-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">Course Catalog</p>
        <p className="text-sm">Coming soon in Phase 2</p>
      </Card>
    </div>
  )
}

