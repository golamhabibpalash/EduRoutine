"use client"

import { useEffect } from "react"
import { PageHeader } from "@/components/layout/page-header"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Save, Bell, Shield, Building, Palette, Loader2 } from "lucide-react"
import { useTheme } from "next-themes"
import { useSettings } from "@/hooks/use-settings"

export function SettingsPage() {
  const { settings, update, save, saving, saved, loading } = useSettings()

  const { theme: activeTheme, setTheme } = useTheme()

  useEffect(() => {
    if (settings.appearance.theme && settings.appearance.theme !== activeTheme) {
      setTheme(settings.appearance.theme)
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <PageHeader title="Settings" description="Configure institution and application settings" />

      <Tabs defaultValue="general">
        <TabsList>
          <TabsTrigger value="general">
            <Building className="mr-2 h-4 w-4" /> General
          </TabsTrigger>
          <TabsTrigger value="notifications">
            <Bell className="mr-2 h-4 w-4" /> Notifications
          </TabsTrigger>
          <TabsTrigger value="security">
            <Shield className="mr-2 h-4 w-4" /> Security
          </TabsTrigger>
          <TabsTrigger value="appearance">
            <Palette className="mr-2 h-4 w-4" /> Appearance
          </TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-4 mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Institution Details</CardTitle>
              <CardDescription>Configure your institution&apos;s basic information</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Institution Name</Label>
                  <Input
                    value={settings.institution.institution_name}
                    onChange={(e) => update("institution", { ...settings.institution, institution_name: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label>Institution Code</Label>
                  <Input
                    value={settings.institution.institution_code}
                    onChange={(e) => update("institution", { ...settings.institution, institution_code: e.target.value.toUpperCase() })}
                  />
                </div>
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Timezone</Label>
                  <select
                    value={settings.institution.timezone}
                    onChange={(e) => update("institution", { ...settings.institution, timezone: e.target.value })}
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  >
                    <option value="Asia/Dhaka">Asia/Dhaka (UTC+6)</option>
                    <option value="Asia/Kolkata">Asia/Kolkata (UTC+5:30)</option>
                    <option value="UTC">UTC</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <Label>Academic Year</Label>
                  <Input
                    value={settings.institution.academic_year}
                    onChange={(e) => update("institution", { ...settings.institution, academic_year: e.target.value })}
                  />
                </div>
              </div>
              <Button onClick={save} disabled={saving || saved}>
                <Save className="mr-2 h-4 w-4" />
                {saving ? "Saving..." : saved ? "Saved!" : "Save Changes"}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-4 mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <CardDescription>Configure when and how you receive notifications</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {[
                { id: "email_schedule", label: "Email - Schedule changes", key: "email_schedule" as const },
                { id: "email_conflicts", label: "Email - Conflict alerts", key: "email_conflicts" as const },
                { id: "email_reports", label: "Email - Weekly reports", key: "email_reports" as const },
                { id: "push_schedule", label: "Push - Schedule changes", key: "push_schedule" as const },
                { id: "push_conflicts", label: "Push - Conflict alerts", key: "push_conflicts" as const },
              ].map(({ id, label, key }) => (
                <label key={id} className="flex items-center justify-between rounded-lg border p-3 cursor-pointer">
                  <span className="text-sm">{label}</span>
                  <Checkbox
                    checked={settings.notifications[key]}
                    onCheckedChange={(v) =>
                      update("notifications", { ...settings.notifications, [key]: v === true })
                    }
                  />
                </label>
              ))}
              <Button onClick={save} disabled={saving || saved}>
                <Save className="mr-2 h-4 w-4" />
                {saving ? "Saving..." : saved ? "Saved!" : "Save Preferences"}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-4 mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Security Settings</CardTitle>
              <CardDescription>Manage authentication and access control</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Session Timeout (minutes)</Label>
                <Input
                  type="number"
                  value={settings.security.session_timeout_minutes}
                  onChange={(e) => update("security", { ...settings.security, session_timeout_minutes: Number(e.target.value) })}
                  min={5}
                  max={480}
                  className="max-w-xs"
                />
              </div>
              <div className="space-y-2">
                <Label>Max Login Attempts</Label>
                <Input
                  type="number"
                  value={settings.security.max_login_attempts}
                  onChange={(e) => update("security", { ...settings.security, max_login_attempts: Number(e.target.value) })}
                  min={3}
                  max={20}
                  className="max-w-xs"
                />
              </div>
              <label className="flex items-center gap-3 cursor-pointer">
                <Checkbox
                  checked={settings.security.require_2fa_admin}
                  onCheckedChange={(v) => update("security", { ...settings.security, require_2fa_admin: v === true })}
                />
                <span className="text-sm">Require two-factor authentication for admin users</span>
              </label>
              <label className="flex items-center gap-3 cursor-pointer">
                <Checkbox
                  checked={settings.security.ip_whitelist_admin}
                  onCheckedChange={(v) => update("security", { ...settings.security, ip_whitelist_admin: v === true })}
                />
                <span className="text-sm">Enable IP whitelist for admin access</span>
              </label>
              <Button onClick={save} disabled={saving || saved}>
                <Save className="mr-2 h-4 w-4" />
                {saving ? "Saving..." : saved ? "Saved!" : "Save Security Settings"}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="appearance" className="space-y-4 mt-4">
          <Card>
            <CardHeader>
              <CardTitle>Appearance</CardTitle>
              <CardDescription>Customize the look and feel of the application</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Theme</Label>
                <div className="flex gap-3">
                  {(["light", "dark", "system"] as const).map((t) => (
                    <label
                      key={t}
                      className={`flex cursor-pointer items-center gap-2 rounded-lg border p-3 hover:bg-muted/50 ${
                        settings.appearance.theme === t ? "border-primary bg-primary/5" : ""
                      }`}
                    >
                      <input
                        type="radio"
                        name="theme"
                        checked={settings.appearance.theme === t}
                        onChange={() => {
                          update("appearance", { ...settings.appearance, theme: t })
                          setTheme(t)
                        }}
                        className="h-4 w-4 text-primary"
                      />
                      <span className="text-sm capitalize">{t}</span>
                    </label>
                  ))}
                </div>
              </div>
              <div className="space-y-2">
                <Label>Compact Mode</Label>
                <label className="flex items-center gap-3 cursor-pointer">
                  <Checkbox
                    checked={settings.appearance.compact_mode}
                    onCheckedChange={(v) => update("appearance", { ...settings.appearance, compact_mode: v === true })}
                  />
                  <span className="text-sm">Use compact layout for data tables and lists</span>
                </label>
              </div>
              <Button onClick={save} disabled={saving || saved}>
                <Save className="mr-2 h-4 w-4" />
                {saving ? "Saving..." : saved ? "Saved!" : "Save Appearance"}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}