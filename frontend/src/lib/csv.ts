export function parseCSV(text: string): { headers: string[]; rows: Record<string, string>[] } {
  const lines: string[] = []
  let current = ""
  let inQuotes = false

  for (let i = 0; i < text.length; i++) {
    const ch = text[i]
    if (ch === '"') {
      inQuotes = !inQuotes
    } else if (ch === "\n" && !inQuotes) {
      lines.push(current)
      current = ""
    } else if (ch === "\r" && !inQuotes) {
      continue
    } else {
      current += ch
    }
  }
  if (current.trim()) lines.push(current)

  if (lines.length < 2) return { headers: [], rows: [] }

  function splitLine(line: string): string[] {
    const cols: string[] = []
    let cur = ""
    let q = false
    for (let i = 0; i < line.length; i++) {
      const c = line[i]
      if (c === '"') { q = !q }
      else if (c === "," && !q) { cols.push(cur.trim()); cur = "" }
      else { cur += c }
    }
    cols.push(cur.trim())
    return cols
  }

  const headers = splitLine(lines[0]).map(h => h.replace(/^"|"$/g, ""))
  const rows: Record<string, string>[] = []

  for (let i = 1; i < lines.length; i++) {
    const cols = splitLine(lines[i])
    if (cols.length === 0 || (cols.length === 1 && !cols[0])) continue
    const row: Record<string, string> = {}
    headers.forEach((h, idx) => { row[h] = (cols[idx] ?? "").replace(/^"|"$/g, "") })
    rows.push(row)
  }

  return { headers, rows }
}

export function downloadSampleCSV(headers: string[], filename: string) {
  const bom = "\uFEFF"
  const content = bom + headers.join(",") + "\n" + headers.map(() => "").join(",") + "\n"
  const blob = new Blob([content], { type: "text/csv;charset=utf-8" })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}
