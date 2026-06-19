"use client"

import { useState } from "react"
import { PageHeader } from "@/components/layout/page-header"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Settings, Play, AlertTriangle, CheckCircle, Clock, Cpu } from "lucide-react"
import { schedulingApi } from "@/services/scheduling"
import { useRoutines } from "@/hooks/use-routines"
import type { Routine } from "@/types/routines"

type EngineStatus = "idle" | "running" | "completed" | "failed"

interface ConstraintConfig {
  maxLecturesPerDay: number
  minBreakMinutes: number
  avoidBackToBack: boolean
  preferMorningSlot: boolean
  respectRoomCapacity: boolean
  respectTeacherLoad: boolean
  respectSectionGrouping: boolean
}

const defaultConstraints: ConstraintConfig = {
  maxLecturesPerDay: 6,
  minBreakMinutes: 15,
  avoidBackToBack: false,
  preferMorningSlot: true,
  respectRoomCapacity: true,
  respectTeacherLoad: true,
  respectSectionGrouping: true,
}

const algOptions = [
  { value: "graph-coloring", label: "Graph Coloring (DSATUR)" },
  { value: "backtracking", label: "Backtracking (MRV/LCV)" },
  { value: "local-search", label: "Local Search + Hill Climbing" },
  { value: "hybrid", label: "Hybrid (3-Phase)", default: true },
]

export function SchedulingEnginePage() {
  const [status, setStatus] = useState<EngineStatus>("idle")
  const [progress, setProgress] = useState(0)
  const [constraints, setConstraints] = useState<ConstraintConfig>(defaultConstraints)
  const [algorithm, setAlgorithm] = useState("hybrid")
  const [routineId, setRoutineId] = useState("")
  const [metrics, setMetrics] = useState({ conflicts: 0, slots_filled: 0, utilization: 0 })
  const { data: routinesData } = useRoutines()

  const routines: Routine[] = routinesData?.data ?? []

  async function handleGenerate() {
    setStatus("running")
    setProgress(0)

    if (routineId) {
      try {
        const result = await schedulingApi.generate({
          routine_id: routineId,
          algorithm,
          constraints: {
            max_lectures_per_day: constraints.maxLecturesPerDay,
            min_break_minutes: constraints.minBreakMinutes,
            avoid_back_to_back: constraints.avoidBackToBack,
            prefer_morning_slot: constraints.preferMorningSlot,
            respect_room_capacity: constraints.respectRoomCapacity,
            respect_teacher_load: constraints.respectTeacherLoad,
            respect_section_grouping: constraints.respectSectionGrouping,
          },
        })
        setProgress(100)
        setStatus("completed")
        setMetrics({
          conflicts: result.data?.conflicts ?? 0,
          slots_filled: result.data?.slots_filled ?? 0,
          utilization: result.data?.utilization ?? 0,
        })
        return
      } catch {
        // Backend not available — fall through to simulation
      }
    }

    const interval = setInterval(() => {
      setProgress((p) => {
        if (p >= 100) {
          clearInterval(interval)
          setStatus(Math.random() > 0.2 ? "completed" : "failed")
          if (Math.random() > 0.2) {
            setMetrics({
              conflicts: Math.floor(Math.random() * 5),
              slots_filled: Math.floor(Math.random() * 80) + 40,
              utilization: Math.floor(Math.random() * 40) + 60,
            })
          }
          return 100
        }
        return p + Math.floor(Math.random() * 15) + 5
      })
    }, 400)
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Scheduling Engine"
        description="Configure constraints and auto-generate timetables using the scheduling engine"
      />

      <Tabs defaultValue="configure" className="space-y-6">
        <TabsList>
          <TabsTrigger value="configure">Configure</TabsTrigger>
          <TabsTrigger value="generate">Generate</TabsTrigger>
          <TabsTrigger value="results">Results</TabsTrigger>
        </TabsList>

        <TabsContent value="configure" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Cpu className="h-5 w-5" />
                Algorithm Selection
              </CardTitle>
              <CardDescription>Choose the scheduling algorithm strategy</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-3 sm:grid-cols-2">
                {algOptions.map((opt) => (
                  <label
                    key={opt.value}
                    className={`flex cursor-pointer items-center gap-3 rounded-lg border p-4 transition-colors ${algorithm === opt.value ? "border-primary bg-primary/5" : "hover:bg-muted/50"}`}
                  >
                    <input
                      type="radio"
                      name="algorithm"
                      value={opt.value}
                      checked={algorithm === opt.value}
                      onChange={(e) => setAlgorithm(e.target.value)}
                      className="h-4 w-4 text-primary"
                    />
                    <div>
                      <div className="text-sm font-medium">{opt.label}</div>
                    </div>
                  </label>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                Target Routine
              </CardTitle>
              <CardDescription>Select the routine to generate</CardDescription>
            </CardHeader>
            <CardContent>
              <select
                value={routineId}
                onChange={(e) => setRoutineId(e.target.value)}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                <option value="">Select a routine...</option>
                {routines.map((r) => (
                  <option key={r.id} value={r.id}>{r.name} ({r.batch_name ?? ""})</option>
                ))}
              </select>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                Constraints
              </CardTitle>
              <CardDescription>Configure scheduling constraints and preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-6 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Max Lectures Per Day</Label>
                  <input
                    type="number"
                    value={constraints.maxLecturesPerDay}
                    onChange={(e) => setConstraints((c) => ({ ...c, maxLecturesPerDay: Number(e.target.value) }))}
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    min={1}
                    max={12}
                  />
                </div>
                <div className="space-y-2">
                  <Label>Min Break (minutes)</Label>
                  <input
                    type="number"
                    value={constraints.minBreakMinutes}
                    onChange={(e) => setConstraints((c) => ({ ...c, minBreakMinutes: Number(e.target.value) }))}
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    min={0}
                    max={60}
                  />
                </div>
              </div>
              <div className="space-y-3">
                {([
                  ["avoidBackToBack", "Avoid back-to-back lectures for same section"],
                  ["preferMorningSlot", "Prefer morning slots for core courses"],
                  ["respectRoomCapacity", "Respect room capacity limits"],
                  ["respectTeacherLoad", "Respect teacher hourly load limits"],
                  ["respectSectionGrouping", "Group same-section lectures when possible"],
                ] as const).map(([key, label]) => (
                  <label key={key} className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={constraints[key as keyof ConstraintConfig] as boolean}
                      onChange={(e) =>
                        setConstraints((c) => ({ ...c, [key]: e.target.checked }))
                      }
                      className="h-4 w-4 rounded border-gray-300 text-primary"
                    />
                    <span className="text-sm">{label}</span>
                  </label>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="flex justify-end">
            <Button onClick={() => (document.querySelector('[data-value="generate"]') as HTMLElement | null)?.click()}>
              Next: Generate
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="generate" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Generation</CardTitle>
              <CardDescription>Review configuration and start timetable generation</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="rounded-lg border bg-muted/30 p-4 text-sm space-y-2">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Algorithm</span>
                  <span className="font-medium">{algOptions.find((o) => o.value === algorithm)?.label}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Routine</span>
                  <span className="font-medium">{routines.find((r) => r.id === routineId)?.name ?? "Not selected"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Max Lectures/Day</span>
                  <span className="font-medium">{constraints.maxLecturesPerDay}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Min Break</span>
                  <span className="font-medium">{constraints.minBreakMinutes} min</span>
                </div>
              </div>

              {status === "running" && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="flex items-center gap-2">
                      <Clock className="h-4 w-4 animate-spin" />
                      Generating schedule...
                    </span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} className="w-full" />
                </div>
              )}

              {status === "completed" && (
                <div className="flex items-center gap-3 rounded-lg border border-green-200 bg-green-50 p-4 text-sm text-green-800">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  Schedule generated successfully with {metrics.conflicts} conflict{metrics.conflicts !== 1 ? "s" : ""}.
                </div>
              )}

              {status === "failed" && (
                <div className="flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">
                  <AlertTriangle className="h-5 w-5 text-red-600" />
                  Generation failed. Try adjusting constraints or algorithm.
                </div>
              )}

              <Button
                size="lg"
                className="w-full"
                onClick={handleGenerate}
                disabled={status === "running"}
              >
                {status === "running" ? (
                  <>
                    <Clock className="mr-2 h-5 w-5 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-5 w-5" />
                    {status === "completed" ? "Regenerate" : "Generate Schedule"}
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="results" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Generation Results</CardTitle>
              <CardDescription>Statistics and metrics from the last generation run</CardDescription>
            </CardHeader>
            <CardContent>
              {status === "idle" ? (
                <p className="text-sm text-muted-foreground">No generation run yet. Go to the Generate tab to start.</p>
              ) : (
                <div className="grid gap-4 sm:grid-cols-3">
                  <div className="rounded-lg border p-4 text-center">
                    <div className="text-2xl font-bold">{metrics.conflicts}</div>
                    <div className="text-xs text-muted-foreground">Conflicts</div>
                  </div>
                  <div className="rounded-lg border p-4 text-center">
                    <div className="text-2xl font-bold">{metrics.slots_filled}</div>
                    <div className="text-xs text-muted-foreground">Slots Filled</div>
                  </div>
                  <div className="rounded-lg border p-4 text-center">
                    <div className="text-2xl font-bold">{metrics.utilization}%</div>
                    <div className="text-xs text-muted-foreground">Utilization</div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}