"use client"

import { useAuthStore } from "@/store/auth-store"
import { useUsers } from "@/hooks/use-users"
import { useCourses } from "@/hooks/use-courses"
import { useStudents } from "@/hooks/use-students"
import { useTeachers } from "@/hooks/use-teachers"
import { useRooms } from "@/hooks/use-rooms"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Calendar,
  BookOpen,
  GraduationCap,
  UserCircle,
  DoorOpen,
  ArrowRight,
  Clock,
  Users,
} from "lucide-react"
import Link from "next/link"

const quickLinks = [
  { label: "View Routines", href: "/routines", icon: Calendar },
  { label: "Manage Courses", href: "/courses", icon: BookOpen },
  { label: "User Management", href: "/users", icon: Users },
  { label: "Room Directory", href: "/rooms", icon: DoorOpen },
  { label: "Scheduling Engine", href: "/scheduling", icon: Clock },
]

export function DashboardPage() {
  const user = useAuthStore((s) => s.user)
  const { data: usersData } = useUsers()
  const { data: coursesData } = useCourses()
  const { data: studentsData } = useStudents()
  const { data: teachersData } = useTeachers()
  const { data: roomsData } = useRooms()

  const userCount = usersData?.pagination?.total_items ?? usersData?.data?.length ?? 0
  const courseCount = coursesData?.pagination?.total_items ?? coursesData?.data?.length ?? 0
  const studentCount = studentsData?.pagination?.total_items ?? studentsData?.data?.length ?? 0
  const teacherCount = teachersData?.pagination?.total_items ?? teachersData?.data?.length ?? 0
  const roomCount = roomsData?.pagination?.total_items ?? roomsData?.data?.length ?? 0

  const statCards = [
    { title: "Active Routines", icon: Calendar, value: "—", description: "No routines published yet", href: "/routines" },
    { title: "Courses", icon: BookOpen, value: String(courseCount), description: courseCount ? "Total course offerings" : "No courses created yet", href: "/courses" },
    { title: "Students", icon: GraduationCap, value: String(studentCount), description: studentCount ? "Total enrolled" : "No students enrolled yet", href: "/students" },
    { title: "Teachers", icon: UserCircle, value: String(teacherCount), description: teacherCount ? "Faculty members" : "No teachers added yet", href: "/teachers" },
    { title: "Rooms", icon: DoorOpen, value: String(roomCount), description: roomCount ? "Total facilities" : "No rooms added yet", href: "/rooms" },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Welcome{user ? `, ${user.display_name}` : ""}
        </h1>
        <p className="text-muted-foreground mt-1">
          EduRoutine Timetable Management System
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        {statCards.map((card) => {
          const Icon = card.icon
          return (
            <Link key={card.title} href={card.href}>
              <Card className="transition-colors hover:bg-accent/50 cursor-pointer h-full">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">{card.title}</CardTitle>
                  <Icon className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{card.value}</div>
                  <p className="text-xs text-muted-foreground mt-1">{card.description}</p>
                </CardContent>
              </Card>
            </Link>
          )
        })}
      </div>

      <div>
        <h2 className="text-lg font-medium mb-4">Quick Actions</h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
          {quickLinks.map((link) => {
            const Icon = link.icon
            return (
              <Link
                key={link.href}
                href={link.href}
                className="flex items-center justify-between rounded-lg border p-4 transition-colors hover:bg-accent/50"
              >
                <div className="flex items-center gap-3">
                  <Icon className="h-5 w-5 text-muted-foreground" />
                  <span className="text-sm font-medium">{link.label}</span>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
              </Link>
            )
          })}
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">System Overview</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <OverviewRow label="Total Users" value={String(userCount)} />
            <OverviewRow label="Courses" value={String(courseCount)} />
            <OverviewRow label="Students" value={String(studentCount)} />
            <OverviewRow label="Teachers" value={String(teacherCount)} />
            <OverviewRow label="Rooms" value={String(roomCount)} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">Activity log will appear here once the system is in use.</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function OverviewRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between border-b pb-2 last:border-0 last:pb-0">
      <span className="text-sm text-muted-foreground">{label}</span>
      <span className="text-sm font-medium">{value}</span>
    </div>
  )
}
