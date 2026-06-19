"use client"

import { useState } from "react"
import Link from "next/link"
import { PageHeader } from "@/components/layout/page-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download } from "lucide-react"
import { TimetableGrid } from "@/features/routines/components/TimetableGrid"
import { useRooms } from "@/hooks/use-rooms"
import { useRoutineDetails } from "@/hooks/use-routines"
import { useRoutines } from "@/hooks/use-routines"
import { exportToPdf, exportToExcel } from "@/lib/export"
import type { RoutineDetail } from "@/types/routines"

export default function RoomReportRoute() {
  const [roomId, setRoomId] = useState("")
  const [routineId, setRoutineId] = useState("")
  const { data: roomsData } = useRooms()
  const { data: routinesData } = useRoutines()
  const { data: detailsData } = useRoutineDetails(routineId)

  const rooms = roomsData?.data ?? []
  const routines = routinesData?.data ?? []
  const details: RoutineDetail[] = detailsData?.data ?? []
  const roomName = rooms.find((r: { id: string; name: string }) => r.id === roomId)?.name ?? "Room"

  return (
    <div className="space-y-6">
      <PageHeader title="Room Utilization">
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => exportToPdf(details, `${roomName} Utilization`)} disabled={!roomId}><Download className="mr-2 h-4 w-4" /> Export PDF</Button>
          <Button variant="outline" onClick={() => exportToExcel(details, `${roomName} Utilization`)} disabled={!roomId}><Download className="mr-2 h-4 w-4" /> Export Excel</Button>
          <Link href="/reports"><Button variant="outline"><ArrowLeft className="mr-2 h-4 w-4" /> Back</Button></Link>
        </div>
      </PageHeader>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Select Room</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <select value={roomId} onChange={(e) => setRoomId(e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
            <option value="">Choose a room...</option>
            {rooms.map((r: { id: string; name: string; code: string }) => (
              <option key={r.id} value={r.id}>{r.name} ({r.code})</option>
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
      {details.length === 0 && roomId && routineId && (
        <p className="text-sm text-muted-foreground text-center py-8">No schedule data available.</p>
      )}
    </div>
  )
}