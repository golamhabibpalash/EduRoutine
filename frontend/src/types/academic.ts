export interface Session {
  id: string
  name: string
  start_date: string
  end_date: string
  is_current: boolean
  created_at: string
  updated_at: string
}

export interface Batch {
  id: string
  name: string
  session_id: string
  session_name?: string
  section_count?: number
  student_count?: number
  created_at: string
  updated_at: string
}

export interface Semester {
  id: string
  name: string
  code: string
  batch_id: string
  batch_name?: string
  start_date: string
  end_date: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Section {
  id: string
  name: string
  batch_id: string
  batch_name?: string
  student_count?: number
  created_at: string
  updated_at: string
}
