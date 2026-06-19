"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  Calendar,
  BookOpen,
  Users,
  UserCircle,
  DoorOpen,
  ClipboardList,
  BarChart3,
  Settings,
  LayoutDashboard,
  GraduationCap,
  Clock,
  Hourglass,
} from "lucide-react"

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/routines", label: "Routines", icon: Calendar },
  { href: "/periods", label: "Periods", icon: Hourglass },
  { href: "/courses", label: "Courses", icon: BookOpen },
  { href: "/teachers", label: "Teachers", icon: UserCircle },
  { href: "/students", label: "Students", icon: GraduationCap },
  { href: "/rooms", label: "Rooms", icon: DoorOpen },
  { href: "/scheduling", label: "Scheduling", icon: Clock },
  { href: "/reports", label: "Reports", icon: BarChart3 },
  { href: "/users", label: "Users", icon: Users },
  { href: "/settings", label: "Settings", icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="hidden border-r bg-card md:flex md:w-60 lg:w-72">
      <nav className="flex flex-col gap-1 p-4 w-full">
        <div className="flex items-center gap-2 px-3 py-4 mb-4">
          <ClipboardList className="h-6 w-6 text-primary" />
          <span className="text-lg font-semibold">EduRoutine</span>
        </div>
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/")
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
              )}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
