export interface ActivityEvent {
  id: string
  type: "create" | "update" | "delete" | "publish" | "archive" | "generate" | "login"
  entity: string
  summary: string
  timestamp: Date
  userId?: string
  userName?: string
}

const SAMPLE_EVENTS: ActivityEvent[] = [
  { id: "evt-1", type: "login", entity: "user", summary: "Admin user logged in", timestamp: new Date(Date.now() - 1000 * 60 * 5), userName: "Admin User" },
  { id: "evt-2", type: "create", entity: "teacher", summary: "New teacher Dr. Rahman added", timestamp: new Date(Date.now() - 1000 * 60 * 15), userName: "Admin User" },
  { id: "evt-3", type: "create", entity: "course", summary: "Course CS-101 created", timestamp: new Date(Date.now() - 1000 * 60 * 30), userName: "Admin User" },
  { id: "evt-4", type: "publish", entity: "routine", summary: "Routine 'Spring 2026' published", timestamp: new Date(Date.now() - 1000 * 60 * 60), userName: "Admin User" },
  { id: "evt-5", type: "update", entity: "room", summary: "Room 301 capacity updated", timestamp: new Date(Date.now() - 1000 * 60 * 120), userName: "Admin User" },
  { id: "evt-6", type: "generate", entity: "schedule", summary: "Schedule generated for Fall 2026", timestamp: new Date(Date.now() - 1000 * 60 * 180), userName: "Admin User" },
  { id: "evt-7", type: "create", entity: "student", summary: "Batch of 50 students imported", timestamp: new Date(Date.now() - 1000 * 60 * 240), userName: "Admin User" },
  { id: "evt-8", type: "archive", entity: "routine", summary: "Routine 'Fall 2025' archived", timestamp: new Date(Date.now() - 1000 * 60 * 300), userName: "Admin User" },
]

export function getSampleActivityLog(): ActivityEvent[] {
  return SAMPLE_EVENTS
}