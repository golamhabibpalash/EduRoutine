"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { authApi } from "@/services/auth"
import { AuthLayout } from "@/components/layout/auth-layout"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Lock, CheckCircle2, Loader2, ArrowLeft } from "lucide-react"

export function ResetPasswordPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const token = searchParams.get("token") ?? ""

  const [password, setPassword] = useState("")
  const [confirm, setConfirm] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [done, setDone] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (password !== confirm) {
      setError("Passwords do not match.")
      return
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.")
      return
    }
    setLoading(true)
    setError(null)
    try {
      await authApi.resetPassword(token, password)
      setDone(true)
    } catch {
      setError("Failed to reset password. The link may have expired.")
    } finally {
      setLoading(false)
    }
  }

  if (done) {
    return (
      <AuthLayout title="Password reset" description="Your password has been reset successfully.">
        <div className="flex flex-col items-center gap-4 py-4">
          <CheckCircle2 className="h-12 w-12 text-green-500" />
          <Button onClick={() => router.push("/login")}><ArrowLeft className="mr-2 h-4 w-4" /> Go to Login</Button>
        </div>
      </AuthLayout>
    )
  }

  if (!token) {
    return (
      <AuthLayout title="Invalid reset link" description="This password reset link is invalid or has expired.">
        <Link href="/forgot-password"><Button variant="outline" className="w-full">Request a new link</Button></Link>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout title="Set new password" description="Enter your new password below.">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">{error}</div>
        )}
        <div className="space-y-2">
          <Label htmlFor="password">New Password</Label>
          <Input
            id="password"
            type="password"
            placeholder="Min. 8 characters"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="confirm">Confirm Password</Label>
          <Input
            id="confirm"
            type="password"
            placeholder="Repeat your password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
          />
        </div>
        <Button type="submit" className="w-full" disabled={loading}>
          {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          <Lock className="mr-2 h-4 w-4" /> Reset Password
        </Button>
      </form>
    </AuthLayout>
  )
}