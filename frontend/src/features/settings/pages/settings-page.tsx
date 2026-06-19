"use client"

import { useState } from "react"
import { PageHeader } from "@/components/layout/page-header"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Save, Bell, Shield, Building, Palette } from "lucide-react"

export function SettingsPage() {
  const [institutionName, setInstitutionName] = useState("EduRoutine Institute")
  const [institutionCode, setInstitutionCode] = useState("ERI")
  const [timezone, setTimezone] = useState("Asia/Dhaka")
  const [academicYear, setAcademicYear] = useState("2026")
  const [saved, setSaved] = useState(false)

  function handleSave() {
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
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
                  <Input value={institutionName} onChange={(e) => setInstitutionName(e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Institution Code</Label>
                  <Input value={institutionCode} onChange={(e) => setInstitutionCode(e.target.value.toUpperCase())} />
                </div>
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Timezone</Label>
                  <select value={timezone} onChange={(e) => setTimezone(e.target.value)} className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                    <option value="Asia/Dhaka">Asia/Dhaka (UTC+6)</option>
                    <option value="Asia/Kolkata">Asia/Kolkata (UTC+5:30)</option>
                    <option value="UTC">UTC</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <Label>Academic Year</Label>
                  <Input value={academicYear} onChange={(e) => setAcademicYear(e.target.value)} />
                </div>
              </div>
              <Button onClick={handleSave} disabled={saved}>
                <Save className="mr-2 h-4 w-4" />
                {saved ? "Saved!" : "Save Changes"}
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
                { id: "emailSchedule", label: "Email - Schedule changes", checked: true },
                { id: "emailConflicts", label: "Email - Conflict alerts", checked: true },
                { id: "emailReports", label: "Email - Weekly reports", checked: false },
                { id: "pushSchedule", label: "Push - Schedule changes", checked: false },
                { id: "pushConflicts", label: "Push - Conflict alerts", checked: true },
              ].map(({ id, label, checked }) => (
                <label key={id} className="flex items-center justify-between rounded-lg border p-3 cursor-pointer">
                  <span className="text-sm">{label}</span>
                  <input type="checkbox" defaultChecked={checked} className="h-4 w-4 rounded border-gray-300 text-primary" />
                </label>
              ))}
              <Button onClick={handleSave} disabled={saved}>
                <Save className="mr-2 h-4 w-4" />
                {saved ? "Saved!" : "Save Preferences"}
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
                <Input type="number" defaultValue={60} min={5} max={480} className="max-w-xs" />
              </div>
              <div className="space-y-2">
                <Label>Max Login Attempts</Label>
                <Input type="number" defaultValue={5} min={3} max={20} className="max-w-xs" />
              </div>
              <label className="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" defaultChecked className="h-4 w-4 rounded border-gray-300 text-primary" />
                <span className="text-sm">Require two-factor authentication for admin users</span>
              </label>
              <label className="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" defaultChecked className="h-4 w-4 rounded border-gray-300 text-primary" />
                <span className="text-sm">Enable IP whitelist for admin access</span>
              </label>
              <Button onClick={handleSave} disabled={saved}>
                <Save className="mr-2 h-4 w-4" />
                {saved ? "Saved!" : "Save Security Settings"}
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
                  {["Light", "Dark", "System"].map((t) => (
                    <label key={t} className="flex cursor-pointer items-center gap-2 rounded-lg border p-3 hover:bg-muted/50">
                      <input type="radio" name="theme" defaultChecked={t === "System"} className="h-4 w-4 text-primary" />
                      <span className="text-sm">{t}</span>
                    </label>
                  ))}
                </div>
              </div>
              <div className="space-y-2">
                <Label>Compact Mode</Label>
                <label className="flex items-center gap-3 cursor-pointer">
                  <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-primary" />
                  <span className="text-sm">Use compact layout for data tables and lists</span>
                </label>
              </div>
              <Button onClick={handleSave} disabled={saved}>
                <Save className="mr-2 h-4 w-4" />
                {saved ? "Saved!" : "Save Appearance"}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
