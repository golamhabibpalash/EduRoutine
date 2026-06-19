"use client"

import Link from "next/link"
import { PageHeader } from "@/components/layout/page-header"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download } from "lucide-react"
import { TimetableGrid } from "@/features/routines/components/TimetableGrid"

export default function MasterReportRoute() {
  return (
    <div className="space-y-6">
      <PageHeader title="Master Timetable">
        <div className="flex gap-2">
          <Button variant="outline"><Download className="mr-2 h-4 w-4" /> Export PDF</Button>
          <Button variant="outline"><Download className="mr-2 h-4 w-4" /> Export Excel</Button>
          <Link href="/reports"><Button variant="outline"><ArrowLeft className="mr-2 h-4 w-4" /> Back</Button></Link>
        </div>
      </PageHeader>
      <TimetableGrid details={[]} />
    </div>
  )
}
