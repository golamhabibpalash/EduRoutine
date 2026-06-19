"use client"

import { useState } from "react"
import Link from "next/link"
import { PageHeader } from "@/components/layout/page-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download } from "lucide-react"
import { TimetableGrid } from "@/features/routines/components/TimetableGrid"
import { useStudents } from "@/hooks/use-students"
import { reportsApi } from "@/services/scheduling"
import { useRoutineDetails } from "@/hooks/use-routines"
import { useRoutines } from "@/hooks/use-routines"
import { exportToPdf, exportToExcel } from "@/lib/export"
import type { RoutineDetail } from "@/types/routines"

export default function StudentReportRoute() {
  const [studentId, setStudentId] = useState("")
  const [routineId, setRoutineId] = useState("")
  const { data: studentsData } = useStudents()
  const { data: routinesData } = useRoutines()
  const { data: detailsData } = useRoutineDetails(routineId)

  const students = studentsData?.data ?? []
  const routines = routinesData?.data ?? []
  const details: RoutineDetail[] = detailsData?.data ?? []
  const studentName = students.find((s: { id: string; name: string }) => s.id === studentId)?.name ?? "Student"

  async function handleExport() {
    try { await reportsApi.studentSchedule({ student_id: studentId }) } catch { /* fallback */ }
  }

  return (
    <div className="space-y-6">
      <PageHeader title="Student Schedule">
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => exportToPdf(details, `${studentName} Schedule`)} disabled={!studentId}><Download className="mr-2 h-4 w-4" /> Export PDF</Button>
          <Button variant="outline" onClick={() => exportToExcel(details, `${studentName} Schedule`)} disabled={!studentId}><Download className="mr-2 h-4 w-4" /> Export Excel</Button>
          <Link href="/reports"><Button variant="outline"><ArrowLeft className="mr-2 h-4 w-4" /> Back</Button></Link>
        </div>
      </PageHeader>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Select Student</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <select value={studentId} onChange={(e) => setStudentId(e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
            <option value="">Choose a student...</option>
            {students.map((s: { id: string; name: string; student_id: string }) => (
              <option key={s.id} value={s.id}>{s.name} ({s.student_id})</option>
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
      {details.length === 0 && studentId && routineId && (
        <p className="text-sm text-muted-foreground text-center py-8">No schedule data available.</p>
      )}
    </div>
  )
}