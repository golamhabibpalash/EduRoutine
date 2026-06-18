"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Calendar, BookOpen, Users, DoorOpen } from "lucide-react"

const placeholderCards = [
  { title: "Active Routines", value: "—", icon: Calendar, description: "No routines loaded" },
  { title: "Courses", value: "—", icon: BookOpen, description: "No courses loaded" },
  { title: "Students", value: "—", icon: Users, description: "No students loaded" },
  { title: "Rooms", value: "—", icon: DoorOpen, description: "No rooms loaded" },
]

export function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">Welcome to EduRoutine. Select a module to get started.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {placeholderCards.map((card) => {
          const Icon = card.icon
          return (
            <Card key={card.title}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{card.title}</CardTitle>
                <Icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{card.value}</div>
                <p className="text-xs text-muted-foreground">{card.description}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
