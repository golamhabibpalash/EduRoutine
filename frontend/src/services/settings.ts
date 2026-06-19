import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"

export interface InstitutionSettings {
  institution_name: string
  institution_code: string
  timezone: string
  academic_year: string
}

export interface NotificationSettings {
  email_schedule: boolean
  email_conflicts: boolean
  email_reports: boolean
  push_schedule: boolean
  push_conflicts: boolean
}

export interface SecuritySettings {
  session_timeout_minutes: number
  max_login_attempts: number
  require_2fa_admin: boolean
  ip_whitelist_admin: boolean
}

export interface AppearanceSettings {
  theme: "light" | "dark" | "system"
  compact_mode: boolean
}

export interface AppSettings {
  institution: InstitutionSettings
  notifications: NotificationSettings
  security: SecuritySettings
  appearance: AppearanceSettings
}

const SETTINGS_KEY = "eduroutine_settings"

const DEFAULT_SETTINGS: AppSettings = {
  institution: {
    institution_name: "EduRoutine Institute",
    institution_code: "ERI",
    timezone: "Asia/Dhaka",
    academic_year: "2026",
  },
  notifications: {
    email_schedule: true,
    email_conflicts: true,
    email_reports: false,
    push_schedule: false,
    push_conflicts: true,
  },
  security: {
    session_timeout_minutes: 60,
    max_login_attempts: 5,
    require_2fa_admin: true,
    ip_whitelist_admin: true,
  },
  appearance: {
    theme: "system",
    compact_mode: false,
  },
}

export const settingsApi = {
  async get(): Promise<AppSettings> {
    return apiClient.get(`${API_PREFIX}/settings`).then((r) => r.data)
  },
  async save(settings: AppSettings): Promise<AppSettings> {
    return apiClient.put(`${API_PREFIX}/settings`, settings).then((r) => r.data)
  },
}

export function loadSettings(): AppSettings {
  if (typeof window === "undefined") return DEFAULT_SETTINGS
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    if (raw) {
      return { ...DEFAULT_SETTINGS, ...JSON.parse(raw) }
    }
  } catch { /* ignore corrupt data */ }
  return DEFAULT_SETTINGS
}

export function saveSettings(settings: AppSettings): void {
  if (typeof window === "undefined") return
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings))
}