import type { HTMLAttributes } from "react"
import { cn } from "@/lib/utils"

type BadgeVariant = "default" | "secondary" | "destructive" | "outline"

const variantStyles: Record<BadgeVariant, string> = {
  default: "border-transparent bg-primary text-primary-foreground",
  secondary: "border-transparent bg-secondary text-secondary-foreground",
  destructive: "border-transparent bg-destructive text-destructive-foreground",
  outline: "text-foreground",
}

interface BadgeProps extends HTMLAttributes<HTMLDivElement> {
  variant?: BadgeVariant
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors",
        variantStyles[variant],
        className,
      )}
      {...props}
    />
  )
}
