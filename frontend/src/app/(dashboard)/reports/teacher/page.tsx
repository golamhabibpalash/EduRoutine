"use client"

import { useState } from "react"
import Link from "next/link"
import { PageHeader } from "@/components/layout/page-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download } from "lucide-react"
import { TimetableGrid } from "@/features/routines/components/TimetableGrid"
import { useTeachers } from "@/hooks/use-teachers"
import { useRoutineDetails } from "@/hooks/use-routines"
import { useRoutines } from "@/hooks/use-routines"
import { exportToPdf, exportToExcel } from "@/lib/export"
import type { RoutineDetail } from "@/types/routines"

export default function TeacherReportRoute() {
  const [teacherId, setTeacherId] = useState("")
  const [routineId, setRoutineId] = useState("")
  const { data: teachersData } = useTeachers()
  const { data: routinesData } = useRoutines()
  const { data: detailsData } = useRoutineDetails(routineId)

  const teachers = teachersData?.data ?? []
  const routines = routinesData?.data ?? []
  const details: RoutineDetail[] = detailsData?.data ?? []
  const teacherName = teachers.find((t: { id: string; name: string }) => t.id === teacherId)?.name ?? "Teacher"

  return (
    <div className="space-y-6">
      <PageHeader title="Teacher Schedule">
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => exportToPdf(details, `${teacherName} Schedule`)} disabled={!teacherId}><Download className="mr-2 h-4 w-4" /> Export PDF</Button>
          <Button variant="outline" onClick={() => exportToExcel(details, `${teacherName} Schedule`)} disabled={!teacherId}><Download className="mr-2 h-4 w-4" /> Export Excel</Button>
          <Link href="/reports"><Button variant="outline"><ArrowLeft className="mr-2 h-4 w-4" /> Back</Button></Link>
        </div>
      </PageHeader>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Select Teacher</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <select value={teacherId} onChange={(e) => setTeacherId(e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
            <option value="">Choose a teacher...</option>
            {teachers.map((t: { id: string; name: string; employee_id: string }) => (
              <option key={t.id} value={t.id}>{t.name} ({t.employee_id})</option>
            ))}
          </select>
          <select value={routineId} onChange={(e) => setRoutineId(e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
            <option value="">Choose a routine...</option>
            {routines.map((r: { id: string; name: string }) => (
              <option key={r.id} value={r.id}>{r.name}</option>
            ))}
          </select>
        </CardContent>
      </Card>
      {details.length > 0 && <TimetableGrid details={details} />}
      {details.length === 0 && teacherId && routineId && (
        <p className="text-sm text-muted-foreground text-center py-8">No schedule data available.</p>
      )}
    </div>
  )
}