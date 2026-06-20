export type DayOfWeek = "saturday" | "sunday" | "monday" | "tuesday" | "wednesday" | "thursday" | "friday"

export type RoutineStatus = "draft" | "published" | "archived"

export interface TimeSlot {
  id: string
  name: string
  day_of_week: DayOfWeek
  start_time: string
  end_time: string
  is_active: boolean
}

export interface Period {
  id: string
  name: string
  period_number: number
  start_time: string
  end_time: string
  duration_minutes: number
  is_break: boolean
  slot_count?: number
}

export interface Routine {
  id: string
  name: string
  session_id: string
  session_name?: string
  batch_id: string
  batch_name?: string
  semester_id: string
  semester_name?: string
  department_id: string
  department_name?: string
  status: RoutineStatus
  version: number
  published_at: string | null
  created_at: string
  updated_at: string
}

export interface RoutineDetail {
  id: string
  routine_id: string
  course_id: string
  course_code?: string
  course_name?: string
  teacher_id: string
  teacher_name?: string
  room_id: string
  room_code?: string
  section_id: string
  section_name?: string
  period_id?: string | null
  day_of_week: DayOfWeek
  start_time: string
  end_time: string
  is_lab: boolean
}

export interface RoutineConflict {
  type: "room" | "teacher" | "student" | "time"
  description: string
  detail_ids: string[]
  severity: "error" | "warning"
}
