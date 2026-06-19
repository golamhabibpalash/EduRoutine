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

export function CreateRoutinePage() {
  const router = useRouter()
  const [name, setName] = useState("")
  const [sessionId, setSessionId] = useState("")
  const [batchId, setBatchId] = useState("")
  const [semesterId, setSemesterId] = useState("")
  const [departmentId, setDepartmentId] = useState("")

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    router.push("/routines")
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
              <Input
                id="department"
                value={departmentId}
                onChange={(e) => setDepartmentId(e.target.value)}
                placeholder="Select department..."
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="session">Session</Label>
              <Input
                id="session"
                value={sessionId}
                onChange={(e) => setSessionId(e.target.value)}
                placeholder="e.g. 2026"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="batch">Batch</Label>
                <Input
                  id="batch"
                  value={batchId}
                  onChange={(e) => setBatchId(e.target.value)}
                  placeholder="e.g. CSE 48"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="semester">Semester</Label>
                <Input
                  id="semester"
                  value={semesterId}
                  onChange={(e) => setSemesterId(e.target.value)}
                  placeholder="e.g. 6th"
                />
              </div>
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <Button type="button" variant="outline" onClick={() => router.back()}>
                Cancel
              </Button>
              <Button type="submit">Create Routine</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
