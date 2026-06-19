"use client"

import { createContext, useContext, useState, useId, useCallback, type ReactNode } from "react"
import { cn } from "@/lib/utils"

interface DialogContextValue {
  open: boolean
  onOpenChange: (open: boolean) => void
  titleId: string
  descriptionId: string
}

const DialogContext = createContext<DialogContextValue | null>(null)

function useDialog() {
  const ctx = useContext(DialogContext)
  if (!ctx) throw new Error("Dialog components must be used within a Dialog")
  return ctx
}

interface DialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  children: ReactNode
}

export function Dialog({ open, onOpenChange, children }: DialogProps) {
  const titleId = useId()
  const descriptionId = useId()
  return (
    <DialogContext.Provider value={{ open, onOpenChange, titleId, descriptionId }}>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm"
            onClick={() => onOpenChange(false)}
          />
          {children}
        </div>
      )}
    </DialogContext.Provider>
  )
}

interface DialogContentProps {
  className?: string
  children: ReactNode
}

export function DialogContent({ className, children }: DialogContentProps) {
  const { titleId, descriptionId } = useDialog()
  return (
    <div
      role="dialog"
      aria-labelledby={titleId}
      aria-describedby={descriptionId}
      className={cn(
        "relative z-50 w-full max-w-lg rounded-lg border bg-background p-6 shadow-lg",
        className,
      )}
    >
      {children}
    </div>
  )
}

interface DialogHeaderProps {
  className?: string
  children: ReactNode
}

export function DialogHeader({ className, children }: DialogHeaderProps) {
  return <div className={cn("mb-4", className)}>{children}</div>
}

interface DialogTitleProps {
  className?: string
  children: ReactNode
}

export function DialogTitle({ className, children }: DialogTitleProps) {
  const { titleId } = useDialog()
  return (
    <h2 id={titleId} className={cn("text-lg font-semibold leading-none tracking-tight", className)}>
      {children}
    </h2>
  )
}

interface DialogDescriptionProps {
  className?: string
  children: ReactNode
}

export function DialogDescription({ className, children }: DialogDescriptionProps) {
  const { descriptionId } = useDialog()
  return (
    <p id={descriptionId} className={cn("mt-2 text-sm text-muted-foreground", className)}>
      {children}
    </p>
  )
}

interface DialogFooterProps {
  className?: string
  children: ReactNode
}

export function DialogFooter({ className, children }: DialogFooterProps) {
  return <div className={cn("mt-6 flex items-center justify-end gap-2", className)}>{children}</div>
}
