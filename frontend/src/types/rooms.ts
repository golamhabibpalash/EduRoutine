export type RoomType = "classroom" | "lab" | "lecture_hall" | "seminar_room" | "conference_room"

export interface Room {
  id: string
  code: string
  name: string
  type: RoomType
  capacity: number
  building: string
  floor: number
  has_projector: boolean
  has_computers: boolean
  has_ac: boolean
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Lab {
  id: string
  code: string
  name: string
  capacity: number
  building: string
  floor: number
  equipment: string[]
  has_projector: boolean
  is_active: boolean
  created_at: string
  updated_at: string
}
