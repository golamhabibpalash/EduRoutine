"use client"

import { PageHeader } from "@/components/layout/page-header"
import { Settings } from "lucide-react"
import { Card } from "@/components/ui/card"

export function SettingsPage() {
  return (
    <div>
      <PageHeader
        title="Application Settings"
        description="Configure institution and application settings"
      />
      <Card className="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <Settings className="h-12 w-12 mb-4 opacity-40" />
        <p className="text-lg font-medium">Application Settings</p>
        <p className="text-sm">Coming soon in Phase 2</p>
      </Card>
    </div>
  )
}

