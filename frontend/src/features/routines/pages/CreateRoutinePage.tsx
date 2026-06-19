"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { PageHeader } from "@/components/layout/page-header"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent } from "@/components/ui/card"
import { ArrowLeft } from "lucide-react"
import Link from "next/link"
import { useDepartments, useSessions, useBatches, useSemesters } from "@/hooks/use-academic"
import { useCreateRoutine } from "@/hooks/use-routines"

export function CreateRoutinePage() {
  const router = useRouter()
  const [name, setName] = useState("")
  const [departmentId, setDepartmentId] = useState("")
  const [sessionId, setSessionId] = useState("")
  const [batchId, setBatchId] = useState("")
  const [semesterId, setSemesterId] = useState("")

  const { data: deptData } = useDepartments()
  const { data: sessData } = useSessions()
  const { data: batchData } = useBatches()
  const { data: semData } = useSemesters()
  const createMutation = useCreateRoutine()

  const departments = deptData?.data ?? []
  const sessions = sessData?.data ?? []
  const allBatches = batchData?.data ?? []
  const semesters = semData?.data ?? []

  const filteredBatches = allBatches.filter((b: { department_id: string; session_id: string }) =>
    (!departmentId || b.department_id === departmentId) &&
    (!sessionId || b.session_id === sessionId)
  )

  const filteredSemesters = semesters.filter((s: { session_id: string }) =>
    !sessionId || s.session_id === sessionId
  )

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    createMutation.mutate(
      { name, department_id: departmentId, session_id: sessionId, batch_id: batchId, semester_id: semesterId },
      { onSuccess: (data) => { router.push(`/routines/${data.id}`) } },
    )
  }

  return (
    <div className="space-y-6">
      <PageHeader title="New Routine">
        <Link href="/routines">
          <Button variant="outline">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
        </Link>
      </PageHeader>

      <Card className="max-w-lg">
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Routine Name</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. CSE 48 - 6th Semester"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="department">Department</Label>
              <select
                id="department"
                value={departmentId}
                onChange={(e) => { setDepartmentId(e.target.value); setBatchId("") }}
                required
                className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
              >
                <option value="">Select department...</option>
                {departments.map((d: { id: string; name: string; code: string }) => (
                  <option key={d.id} value={d.id}>{d.name} ({d.code})</option>
                ))}
              </select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="session">Session</Label>
              <select
                id="session"
                value={sessionId}
                onChange={(e) => { setSessionId(e.target.value); setSemesterId("") }}
                required
                className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
              >
                <option value="">Select session...</option>
                {sessions.map((s: { id: string; name: string }) => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="batch">Batch</Label>
                <select
                  id="batch"
                  value={batchId}
                  onChange={(e) => setBatchId(e.target.value)}
                  required
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                >
                  <option value="">Select batch...</option>
                  {filteredBatches.map((b: { id: string; name: string; code: string }) => (
                    <option key={b.id} value={b.id}>{b.name} ({b.code})</option>
                  ))}
                </select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="semester">Semester</Label>
                <select
                  id="semester"
                  value={semesterId}
                  onChange={(e) => setSemesterId(e.target.value)}
                  required
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                >
                  <option value="">Select semester...</option>
                  {filteredSemesters.map((s: { id: string; name: string; number: number }) => (
                    <option key={s.id} value={s.id}>{s.name}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <Button type="button" variant="outline" onClick={() => router.back()}>
                Cancel
              </Button>
              <Button type="submit" disabled={createMutation.isPending}>
                {createMutation.isPending ? "Creating..." : "Create Routine"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}