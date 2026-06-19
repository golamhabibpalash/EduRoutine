export interface Course {
  id: string
  department_id: string
  department_name: string
  code: string
  title: string
  credits: number
  lecture_hours: number
  lab_hours: number
  is_active: boolean
  created_at: string
  updated_at: string
}
