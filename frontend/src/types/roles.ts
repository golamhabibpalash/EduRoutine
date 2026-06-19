export interface Role {
  id: string
  name: string
  description: string | null
  is_system_role: boolean
  permission_count: number
  created_at: string
}

export interface Permission {
  id: string
  code: string
  name: string
  module: string
  description: string | null
}
