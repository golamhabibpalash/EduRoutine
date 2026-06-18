"use client"

import { useAuthStore } from "@/store/auth-store"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Calendar,
  BookOpen,
  Users,
  DoorOpen,
  Clock,
  ArrowRight,
  GraduationCap,
  UserCircle,
} from "lucide-react"
import Link from "next/link"

const statCards = [
  {
    title: "Active Routines",
    icon: Calendar,
    value: "—",
    description: "No routines published yet",
    href: "/routines",
  },
  {
    title: "Courses",
    icon: BookOpen,
    value: "—",
    description: "No courses created yet",
    href: "/courses",
  },
  {
    title: "Students",
    icon: GraduationCap,
    value: "—",
    description: "No students enrolled yet",
    href: "/students",
  },
  {
    title: "Teachers",
    icon: UserCircle,
    value: "—",
    description: "No teachers added yet",
    href: "/teachers",
  },
]

const quickLinks = [
  { label: "View Routines", href: "/routines", icon: Calendar },
  { label: "Manage Courses", href: "/courses", icon: BookOpen },
  { label: "User Management", href: "/users", icon: Users },
  { label: "Room Directory", href: "/rooms", icon: DoorOpen },
  { label: "Scheduling", href: "/scheduling", icon: Clock },
]

export function DashboardPage() {
  const user = useAuthStore((s) => s.user)

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

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((card) => {
          const Icon = card.icon
          return (
            <Link key={card.title} href={card.href}>
              <Card className="transition-colors hover:bg-accent/50 cursor-pointer">
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
    </div>
  )
}
