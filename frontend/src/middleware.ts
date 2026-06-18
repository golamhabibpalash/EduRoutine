import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

const publicPaths = ["/login", "/register", "/forgot-password", "/reset-password", "/auth/callback"]

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const isPublic = publicPaths.some(
    (path) => pathname === path || pathname.startsWith(path),
  )
  const isStatic = pathname.startsWith("/_next") || pathname.startsWith("/favicon")
  const token = request.cookies.get("access_token")?.value

  if (isStatic) {
    return NextResponse.next()
  }

  if (token && isPublic) {
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  if (!token && !isPublic && !pathname.startsWith("/api")) {
    const loginUrl = new URL("/login", request.url)
    loginUrl.searchParams.set("redirect", pathname)
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
}
