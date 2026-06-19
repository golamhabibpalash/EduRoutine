import { Suspense } from "react"
import { ResetPasswordPage } from "@/features/auth/pages/reset-password-page"

export default function ResetPasswordRoute() {
  return (
    <Suspense fallback={<div className="py-12 text-center text-muted-foreground">Loading...</div>}>
      <ResetPasswordPage />
    </Suspense>
  )
}
