export interface Course {
  id: string
  code: string
  name: string
  description: string | null
  credits: number
  lecture_hours: number
  tutorial_hours: number
  lab_hours: number
  total_hours: number
  department: string
  semester_id: string
  semester_name?: string
  is_lab: boolean
  prerequisites: string[]
  created_at: string
  updated_at: string
}
