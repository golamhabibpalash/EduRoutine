export interface Student {
  id: string
  student_id: string
  name: string
  email: string
  phone: string | null
  batch_id: string
  batch_name?: string
  section_id: string
  section_name?: string
  enrollment_year: number
  is_active: boolean
  created_at: string
  updated_at: string
}
