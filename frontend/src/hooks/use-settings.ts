import { useState, useCallback, useEffect } from "react"
import { type AppSettings, settingsApi, loadSettings, saveSettings } from "@/services/settings"

export function useSettings() {
  const [settings, setSettings] = useState<AppSettings>(loadSettings)
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    settingsApi.get()
      .then((remote) => { setSettings(remote); saveSettings(remote) })
      .catch(() => { /* use local */ })
      .finally(() => setLoading(false))
  }, [])

  const update = useCallback(<K extends keyof AppSettings>(section: K, value: AppSettings[K]) => {
    setSettings((prev) => {
      const next = { ...prev, [section]: value }
      saveSettings(next)
      return next
    })
  }, [])

  const save = useCallback(async () => {
    setSaving(true)
    try {
      await settingsApi.save(settings)
      saveSettings(settings)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch {
      saveSettings(settings)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } finally {
      setSaving(false)
    }
  }, [settings])

  return { settings, update, save, saving, saved, loading }
}