"use client"

import { useState } from "react"
import Link from "next/link"
import { authApi } from "@/services/auth"
import { AuthLayout } from "@/components/layout/auth-layout"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Mail, ArrowLeft, CheckCircle2, Loader2 } from "lucide-react"

export function ForgotPasswordPage() {
  const [email, setEmail] = useState("")
  const [sent, setSent] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await authApi.forgotPassword(email)
      setSent(true)
    } catch {
      setError("Failed to send reset email. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  if (sent) {
    return (
      <AuthLayout title="Check your email" description="We've sent a password reset link to your email address.">
        <div className="flex flex-col items-center gap-4 py-4">
          <CheckCircle2 className="h-12 w-12 text-green-500" />
          <p className="text-center text-sm text-muted-foreground">
            If an account with <strong>{email}</strong> exists, you'll receive a reset link shortly.
          </p>
          <Link href="/login">
            <Button variant="outline"><ArrowLeft className="mr-2 h-4 w-4" /> Back to Login</Button>
          </Link>
        </div>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout title="Forgot password?" description="Enter your email and we'll send you a reset link.">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">{error}</div>
        )}
        <div className="space-y-2">
          <Label htmlFor="email">Email address</Label>
          <Input
            id="email"
            type="email"
            placeholder="name@institution.edu"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
          />
        </div>
        <Button type="submit" className="w-full" disabled={loading}>
          {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          <Mail className="mr-2 h-4 w-4" /> Send Reset Link
        </Button>
      </form>
      <p className="mt-6 text-center text-sm text-muted-foreground">
        <Link href="/login" className="text-primary hover:underline flex items-center justify-center gap-1">
          <ArrowLeft className="h-4 w-4" /> Back to Login
        </Link>
      </p>
    </AuthLayout>
  )
}