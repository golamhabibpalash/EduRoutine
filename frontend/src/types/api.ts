export interface ApiResponse<T> {
  status: "success" | "error"
  data: T
  meta?: {
    request_id: string
    timestamp: string
    version: string
  }
}

export interface ApiError {
  status: "error"
  error: {
    code: string
    message: string
    details?: Record<string, string[]>
    request_id: string
  }
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

export interface PaginationParams {
  page?: number
  page_size?: number
  sort_by?: string
  sort_order?: "asc" | "desc"
  filter?: string
}
