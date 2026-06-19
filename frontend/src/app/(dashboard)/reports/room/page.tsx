"use client"

import Link from "next/link"
import { PageHeader } from "@/components/layout/page-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download } from "lucide-react"
import { TimetableGrid } from "@/features/routines/components/TimetableGrid"

export default function RoomReportRoute() {
  return (
    <div className="space-y-6">
      <PageHeader title="Room Utilization">
        <div className="flex gap-2">
          <Button variant="outline"><Download className="mr-2 h-4 w-4" /> Export</Button>
          <Link href="/reports"><Button variant="outline"><ArrowLeft className="mr-2 h-4 w-4" /> Back</Button></Link>
        </div>
      </PageHeader>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Select Room</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Select a room to view its utilization statistics and schedule.</p>
        </CardContent>
      </Card>
      <TimetableGrid details={[]} />
    </div>
  )
}
