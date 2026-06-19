"use client"

import { useState } from "react"
import { useParams } from "next/navigation"
import Link from "next/link"
import { useUser } from "@/hooks/use-users"
import { PageHeader } from "@/components/layout/page-header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Mail, Phone, Calendar, Shield, UserCog } from "lucide-react"
import { AssignRolesDialog } from "@/features/users/components/AssignRolesDialog"

export function UserDetailPage() {
  const params = useParams()
  const id = params?.id as string
  const { data: user, isLoading } = useUser(id)
  const [rolesOpen, setRolesOpen] = useState(false)

  if (isLoading) return <div className="py-12 text-center text-muted-foreground">Loading user...</div>
  if (!user) return <div className="py-12 text-center text-muted-foreground">User not found.</div>

  return (
    <div className="space-y-6">
      <PageHeader title={user.display_name ?? user.email}>
        <Link href="/users">
          <Button variant="outline">
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Users
          </Button>
        </Link>
      </PageHeader>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-2"><Shield className="h-5 w-5" /> Account Details</span>
              <Button size="sm" variant="outline" onClick={() => setRolesOpen(true)}>
                <UserCog className="mr-2 h-4 w-4" /> Manage Roles
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Status</span>
              <Badge variant={user.is_active ? "default" : "secondary"}>
                {user.is_active ? "Active" : "Inactive"}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Email</span>
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{user.email}</span>
                {user.email_verified && <Badge variant="outline" className="text-xs">Verified</Badge>}
              </div>
            </div>
            {user.phone && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Phone</span>
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{user.phone}</span>
                </div>
              </div>
            )}
            {user.roles.length > 0 && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Roles</span>
                <div className="flex flex-wrap gap-1">
                  {user.roles.map((r) => <Badge key={r} variant="secondary">{r}</Badge>)}
                </div>
              </div>
            )}
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Last Login</span>
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{user.last_login_at ? new Date(user.last_login_at).toLocaleString() : "Never"}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Created</span>
              <span className="text-sm">{new Date(user.created_at).toLocaleDateString()}</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <AssignRolesDialog open={rolesOpen} onOpenChange={setRolesOpen} user={user} />
    </div>
  )
}
