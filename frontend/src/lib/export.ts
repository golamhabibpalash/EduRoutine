import jsPDF from "jspdf"
import autoTable from "jspdf-autotable"
import * as XLSX from "xlsx"
import type { RoutineDetail, DayOfWeek } from "@/types/routines"

const DAY_LABELS: Record<DayOfWeek, string> = {
  saturday: "Saturday",
  sunday: "Sunday",
  monday: "Monday",
  tuesday: "Tuesday",
  wednesday: "Wednesday",
  thursday: "Thursday",
  friday: "Friday",
}

const DAY_ORDER: DayOfWeek[] = ["sunday", "monday", "tuesday", "wednesday", "thursday"]

function buildRows(details: RoutineDetail[]) {
  const times = [...new Set(details.map((d) => d.start_time))].sort()
  if (times.length === 0) return { rows: [], times: [] }

  return {
    rows: times.map((time) => {
      const row: Record<string, string> = { Time: time }
      for (const day of DAY_ORDER) {
        const entry = details.find((d) => d.day_of_week === day && d.start_time === time)
        row[DAY_LABELS[day]] = entry
          ? `${entry.course_code ?? ""} ${entry.course_name ?? ""}\n${entry.teacher_name ?? ""}\n${entry.room_code ?? ""}`
          : ""
      }
      return row
    }),
    times,
  }
}

export function exportToPdf(details: RoutineDetail[], title: string) {
  const doc = new jsPDF()
  doc.text(title, 14, 15)

  const { rows } = buildRows(details)
  if (rows.length === 0) {
    doc.text("No schedule data available.", 14, 25)
    doc.save(`${title.replace(/\s+/g, "_")}.pdf`)
    return
  }

  autoTable(doc, {
    startY: 22,
    head: [["Time", ...DAY_ORDER.map((d) => DAY_LABELS[d])]],
    body: rows.map((r) => [r.Time, ...DAY_ORDER.map((d) => r[DAY_LABELS[d]] || "")]),
    styles: { fontSize: 8, cellPadding: 2 },
    headStyles: { fillColor: [59, 130, 246] },
  })

  doc.save(`${title.replace(/\s+/g, "_")}.pdf`)
}

export function exportToExcel(details: RoutineDetail[], title: string) {
  const { rows } = buildRows(details)

  const data = rows.map((r) => ({
    Time: r.Time,
    ...Object.fromEntries(DAY_ORDER.map((d) => [DAY_LABELS[d], r[DAY_LABELS[d]] || ""])),
  }))

  const wb = XLSX.utils.book_new()
  const ws = XLSX.utils.json_to_sheet(data)

  const colWidths = [{ wch: 8 }, ...DAY_ORDER.map(() => ({ wch: 30 }))]
  ws["!cols"] = colWidths

  XLSX.utils.book_append_sheet(wb, ws, "Schedule")
  XLSX.writeFile(wb, `${title.replace(/\s+/g, "_")}.xlsx`)
}