import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"

export interface SchedulingConfigPayload {
  routine_id: string
  algorithm: string
  constraints: {
    max_lectures_per_day: number
    min_break_minutes: number
    avoid_back_to_back: boolean
    prefer_morning_slot: boolean
    respect_room_capacity: boolean
    respect_teacher_load: boolean
    respect_section_grouping: boolean
  }
}

export const schedulingApi = {
  generate: async (config: SchedulingConfigPayload) => {
    const r = await apiClient.post(`${API_PREFIX}/scheduling/generate`, config)
    return r.data
  },
  status: async (jobId: string) => {
    const r = await apiClient.get(`${API_PREFIX}/scheduling/status/${jobId}`)
    return r.data
  },
  results: async (routineId: string) => {
    const r = await apiClient.get(`${API_PREFIX}/scheduling/results/${routineId}`)
    return r.data
  },
  conflicts: async (routineId: string) => {
    const r = await apiClient.get(`${API_PREFIX}/scheduling/conflicts/${routineId}`)
    return r.data
  },
  constraints: async (routineId: string) => {
    const r = await apiClient.get(`${API_PREFIX}/scheduling/constraints/${routineId}`)
    return r.data
  },
  updateConstraints: async (routineId: string, constraints: SchedulingConfigPayload["constraints"]) => {
    const r = await apiClient.put(`${API_PREFIX}/scheduling/constraints/${routineId}`, constraints)
    return r.data
  },
}

export const reportsApi = {
  studentSchedule: async (params: { student_id?: string; batch_id?: string }) => {
    const r = await apiClient.get(`${API_PREFIX}/reports/student-schedule`, { params })
    return r.data
  },
  teacherSchedule: async (teacherId: string) => {
    const r = await apiClient.get(`${API_PREFIX}/reports/teacher-schedule/${teacherId}`)
    return r.data
  },
  roomUtilization: async (roomId: string) => {
    const r = await apiClient.get(`${API_PREFIX}/reports/room-utilization/${roomId}`)
    return r.data
  },
  masterTimetable: async (routineId: string) => {
    const r = await apiClient.get(`${API_PREFIX}/reports/master-timetable/${routineId}`)
    return r.data
  },
}
