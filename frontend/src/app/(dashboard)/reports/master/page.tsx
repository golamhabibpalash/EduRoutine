"use client"

import { useState } from "react"
import Link from "next/link"
import { PageHeader } from "@/components/layout/page-header"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download } from "lucide-react"
import { TimetableGrid } from "@/features/routines/components/TimetableGrid"
import { useRoutineDetails } from "@/hooks/use-routines"
import { useRoutines } from "@/hooks/use-routines"
import { exportToPdf, exportToExcel } from "@/lib/export"
import type { RoutineDetail } from "@/types/routines"

export default function MasterReportRoute() {
  const [routineId, setRoutineId] = useState("")
  const { data: routinesData } = useRoutines()
  const { data: detailsData } = useRoutineDetails(routineId)

  const routines = routinesData?.data ?? []
  const details: RoutineDetail[] = detailsData?.data ?? []
  const routineName = routines.find((r: { id: string; name: string }) => r.id === routineId)?.name ?? "Master Timetable"

  return (
    <div className="space-y-6">
      <PageHeader title="Master Timetable">
        <div className="flex gap-2">
          <select value={routineId} onChange={(e) => setRoutineId(e.target.value)}
            className="flex h-9 rounded-md border border-input bg-background px-3 py-1 text-sm">
            <option value="">Select routine...</option>
            {routines.map((r: { id: string; name: string }) => (
              <option key={r.id} value={r.id}>{r.name}</option>
            ))}
          </select>
          <Button variant="outline" disabled={!routineId} onClick={() => exportToPdf(details, routineName)}><Download className="mr-2 h-4 w-4" /> Export PDF</Button>
          <Button variant="outline" disabled={!routineId} onClick={() => exportToExcel(details, routineName)}><Download className="mr-2 h-4 w-4" /> Export Excel</Button>
          <Link href="/reports"><Button variant="outline"><ArrowLeft className="mr-2 h-4 w-4" /> Back</Button></Link>
        </div>
      </PageHeader>
      {details.length > 0 ? (
        <TimetableGrid details={details} />
      ) : (
        routineId && <p className="text-sm text-muted-foreground text-center py-8">Loading schedule...</p>
      )}
    </div>
  )
}