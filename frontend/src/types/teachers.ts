export interface Teacher {
  id: string
  employee_id: string
  name: string
  email: string
  phone: string | null
  department: string
  specialization: string[]
  max_hours_per_week: number
  is_active: boolean
  created_at: string
  updated_at: string
}
