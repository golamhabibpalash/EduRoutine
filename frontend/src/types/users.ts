export interface User {
  id: string
  email: string
  email_verified: boolean
  display_name: string
  phone: string | null
  is_active: boolean
  roles: string[]
  last_login_at: string | null
  created_at: string
  updated_at: string
}

export interface UserFilters {
  search?: string
  is_active?: boolean
  page?: number
  page_size?: number
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    page_size: number
    total_items: number
    total_pages: number
    has_next: boolean
    has_previous: boolean
  }
}
