export interface Department {
  id: string
  name: string
  code: string
  created_at: string
  updated_at: string
}

export interface Session {
  id: string
  name: string
  start_date: string
  end_date: string
  is_current: boolean
  created_at: string
  updated_at: string
}

export interface Semester {
  id: string
  session_id: string
  name: string
  number: number
  start_date: string
  end_date: string
  created_at: string
  updated_at: string
}

export interface Batch {
  id: string
  session_id: string
  department_id: string
  name: string
  code: string
  created_at: string
  updated_at: string
}

export interface Section {
  id: string
  batch_id: string
  name: string
  max_capacity: number
  created_at: string
  updated_at: string
}

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
