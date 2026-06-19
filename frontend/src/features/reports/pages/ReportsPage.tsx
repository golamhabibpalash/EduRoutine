"use client"

import { PageHeader } from "@/components/layout/page-header"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileText, Users, GraduationCap, DoorOpen, Calendar, Download } from "lucide-react"
import Link from "next/link"

const reportCards = [
  {
    title: "Student Schedule",
    description: "View timetable for individual students or entire batch",
    icon: Users,
    href: "/reports/student",
    color: "text-blue-600",
  },
  {
    title: "Teacher Schedule",
    description: "Weekly lecture schedule grouped by teacher",
    icon: GraduationCap,
    href: "/reports/teacher",
    color: "text-green-600",
  },
  {
    title: "Room Utilization",
    description: "Room usage statistics and availability analysis",
    icon: DoorOpen,
    href: "/reports/room",
    color: "text-amber-600",
  },
  {
    title: "Master Timetable",
    description: "Complete routine with all sections side by side",
    icon: Calendar,
    href: "/reports/master",
    color: "text-violet-600",
  },
]

export function ReportsPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Reports"
        description="Generate and export schedule reports"
      />

      <div className="grid gap-4 sm:grid-cols-2">
        {reportCards.map((report) => (
          <Card key={report.title} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-base">
                <report.icon className={`h-5 w-5 ${report.color}`} />
                {report.title}
              </CardTitle>
              <CardDescription>{report.description}</CardDescription>
            </CardHeader>
            <CardContent className="flex gap-2">
              <Link href={report.href}>
                <Button size="sm" variant="outline">
                  <FileText className="mr-2 h-4 w-4" />
                  View
                </Button>
              </Link>
              <Button size="sm" variant="outline">
                <Download className="mr-2 h-4 w-4" />
                Export
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
