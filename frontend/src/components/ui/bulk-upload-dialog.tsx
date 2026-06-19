"use client"

import { useState, useRef, useCallback } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { parseCSV, downloadSampleCSV } from "@/lib/csv"
import { Upload, Download, AlertTriangle, CheckCircle, X, FileText } from "lucide-react"

export interface FieldMapping {
  header: string
  field: string
  required: boolean
}

interface BulkUploadDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  title: string
  description: string
  sampleFilename: string
  fieldMappings: FieldMapping[]
  onUpload: (items: Record<string, string>[]) => Promise<{ success: number; errors: string[] }>
}

type Step = "upload" | "preview" | "result"

export function BulkUploadDialog({
  open,
  onOpenChange,
  title,
  description,
  sampleFilename,
  fieldMappings,
  onUpload,
}: BulkUploadDialogProps) {
  const [step, setStep] = useState<Step>("upload")
  const [headers, setHeaders] = useState<string[]>([])
  const [rows, setRows] = useState<Record<string, string>[]>([])
  const [selectedRows, setSelectedRows] = useState<Set<number>>(new Set())
  const [validationErrors, setValidationErrors] = useState<string[]>([])
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState<{ success: number; errors: string[] } | null>(null)
  const [dragOver, setDragOver] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const requiredFields = fieldMappings.filter((m) => m.required).map((m) => m.header)

  function reset() {
    setStep("upload")
    setHeaders([])
    setRows([])
    setSelectedRows(new Set())
    setValidationErrors([])
    setResult(null)
  }

  function handleFile(file: File | undefined) {
    if (!file) return
    const reader = new FileReader()
    reader.onload = (e) => {
      const text = e.target?.result as string
      const parsed = parseCSV(text)
      if (parsed.rows.length === 0) {
        setValidationErrors(["No valid rows found in the file."])
        return
      }

      const missingFields = requiredFields.filter((f) => !parsed.headers.includes(f))
      if (missingFields.length > 0) {
        setValidationErrors([`Missing required columns: ${missingFields.join(", ")}`])
        return
      }

      setHeaders(parsed.headers)
      setRows(parsed.rows)
      setSelectedRows(new Set(parsed.rows.map((_, i) => i)))
      setValidationErrors([])
      setStep("preview")
    }
    reader.readAsText(file)
  }

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    handleFile(e.dataTransfer.files[0])
  }, [])

  function toggleRow(idx: number) {
    setSelectedRows((prev) => {
      const next = new Set(prev)
      if (next.has(idx)) next.delete(idx)
      else next.add(idx)
      return next
    })
  }

  function toggleAll() {
    if (selectedRows.size === rows.length) {
      setSelectedRows(new Set())
    } else {
      setSelectedRows(new Set(rows.map((_, i) => i)))
    }
  }

  async function handleUpload() {
    const items = rows.filter((_, i) => selectedRows.has(i))
    if (items.length === 0) return
    setUploading(true)
    try {
      const res = await onUpload(items)
      setResult(res)
      setStep("result")
    } catch (err: unknown) {
      setResult({ success: 0, errors: [(err as Error)?.message ?? "Upload failed"] })
      setStep("result")
    } finally {
      setUploading(false)
    }
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(v) => {
        if (!v) reset()
        onOpenChange(v)
      }}
    >
      <DialogContent className="sm:max-w-3xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>

        {step === "upload" && (
          <div className="space-y-4">
            <div
              onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 transition-colors ${dragOver ? "border-primary bg-primary/5" : "border-muted-300 hover:border-muted-400"}`}
            >
              <Upload className="mb-4 h-10 w-10 text-muted-foreground" />
              <p className="text-sm font-medium">Drop your CSV file here, or click to browse</p>
              <p className="mt-1 text-xs text-muted-foreground">Supports .csv files with UTF-8 encoding</p>
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv"
                className="hidden"
                onChange={(e) => handleFile(e.target.files?.[0])}
              />
            </div>

            <div className="flex items-center justify-between">
              <p className="text-xs text-muted-foreground">
                Required columns: {requiredFields.join(", ")}
              </p>
              <Button
                variant="outline"
                size="sm"
                onClick={() => downloadSampleCSV(
                  fieldMappings.map((m) => m.header),
                  sampleFilename,
                )}
              >
                <Download className="mr-2 h-3 w-3" />
                Download Sample
              </Button>
            </div>

            {validationErrors.length > 0 && (
              <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-3">
                {validationErrors.map((err, i) => (
                  <p key={i} className="flex items-center gap-2 text-sm text-destructive">
                    <AlertTriangle className="h-4 w-4" />
                    {err}
                  </p>
                ))}
              </div>
            )}
          </div>
        )}

        {step === "preview" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <p className="text-sm text-muted-foreground">
                {rows.length} rows found, <strong>{selectedRows.size}</strong> selected
              </p>
              <Button variant="outline" size="sm" onClick={() => setStep("upload")}>
                <X className="mr-2 h-3 w-3" />
                Choose different file
              </Button>
            </div>

            <div className="max-h-64 overflow-auto rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-10">
                      <input
                        type="checkbox"
                        checked={selectedRows.size === rows.length}
                        onChange={toggleAll}
                        className="h-4 w-4"
                      />
                    </TableHead>
                    <TableHead>#</TableHead>
                    {headers.map((h) => (
                      <TableHead key={h} className="text-xs font-medium">{h}</TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rows.slice(0, 50).map((row, idx) => (
                    <TableRow
                      key={idx}
                      className={selectedRows.has(idx) ? "" : "opacity-50"}
                    >
                      <TableCell>
                        <input
                          type="checkbox"
                          checked={selectedRows.has(idx)}
                          onChange={() => toggleRow(idx)}
                          className="h-4 w-4"
                        />
                      </TableCell>
                      <TableCell className="text-xs text-muted-foreground font-mono">
                        {idx + 1}
                      </TableCell>
                      {headers.map((h) => (
                        <TableCell key={h} className="text-xs max-w-[150px] truncate">
                          {row[h] || <span className="text-destructive">—</span>}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {rows.length > 50 && (
              <p className="text-xs text-muted-foreground">
                Showing 50 of {rows.length} rows
              </p>
            )}
          </div>
        )}

        {step === "result" && result && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 rounded-lg border p-4">
              {result.errors.length === 0 ? (
                <CheckCircle className="h-6 w-6 text-green-600" />
              ) : (
                <AlertTriangle className="h-6 w-6 text-amber-600" />
              )}
              <div>
                <p className="text-sm font-medium">
                  {result.success} of {result.success + result.errors.length} records uploaded
                </p>
                {result.errors.length > 0 && (
                  <p className="text-xs text-destructive mt-1">
                    {result.errors.length} error{result.errors.length > 1 ? "s" : ""} occurred
                  </p>
                )}
              </div>
            </div>

            {result.errors.length > 0 && (
              <div className="space-y-1">
                {result.errors.map((err, i) => (
                  <p key={i} className="flex items-start gap-2 text-xs text-destructive">
                    <AlertTriangle className="h-3 w-3 mt-0.5 shrink-0" />
                    {err}
                  </p>
                ))}
              </div>
            )}
          </div>
        )}

        <DialogFooter>
          {step === "upload" && (
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
          )}
          {step === "preview" && (
            <>
              <Button variant="outline" onClick={() => reset()}>
                Cancel
              </Button>
              <Button onClick={handleUpload} disabled={selectedRows.size === 0 || uploading}>
                {uploading ? (
                  <>Uploading...</>
                ) : (
                  <>
                    <Upload className="mr-2 h-4 w-4" />
                    Upload {selectedRows.size} Record{selectedRows.size > 1 ? "s" : ""}
                  </>
                )}
              </Button>
            </>
          )}
          {step === "result" && (
            <Button onClick={() => { reset(); onOpenChange(false) }}>
              Done
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
