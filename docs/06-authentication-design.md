# Phase 6: Authentication Design

---

## 27. Authentication Design

### Architecture Overview
```
┌──────────┐     ┌────────────────┐     ┌───────────────┐
│  Client  │────→│  FastAPI Auth  │────→│   Identity    │
│ (Web/App)│     │   Middleware    │     │   Provider    │
└──────────┘     └────────────────┘     └───────────────┘
     │                   │                       │
     │ 1. Login          │ 2. Validate           │ 3. Verify
     │ 4. JWT Response   │ 4. Issue JWT          │ Credentials
     │                   │                       │
     ▼                   ▼                       ▼
┌──────────────────────────────────────────────────────┐
│                    Token Store                         │
│              (Redis - Refresh Token)                   │
└────────────────────────────────────────────────────────┘
```

### Supported Authentication Methods
1. **Email + Password** (local strategy)
2. **Google OAuth2** (OpenID Connect)
3. **Microsoft OAuth2** (Azure AD / Microsoft Account)
4. **Facebook OAuth2** (Facebook Login)

---

## 28. OAuth2 Flow

### Standard Authorization Code Flow (with PKCE)

```
CLIENT                     AUTHORIZATION SERVER              RESOURCE SERVER
  │                              │                                │
  │  1. Auth Request + PKCE      │                                │
  │─────────────────────────────→│                                │
  │                              │                                │
  │  2. User Login & Consent     │                                │
  │  ←──────────────────────────│                                │
  │                              │                                │
  │  3. Authorization Code +     │                                │
  │     code_verifier (PKCE)     │                                │
  │─────────────────────────────→│                                │
  │                              │                                │
  │  4. Exchange Code for Tokens │                                │
  │  ←──────────────────────────│                                │
  │                              │                                │
  │  5. Access Token in Header   │                                │
  │  ────────────────────────────────────────────────────────────→│
  │                              │                                │
  │  6. Validate & Return Data   │                                │
  │  ←────────────────────────────────────────────────────────────│
```

### Social Login Integration

#### Provider Registration
Each OAuth2 provider requires:
- `client_id` (public)
- `client_secret` (encrypted at rest)
- `redirect_uri` (per environment)
- `authorization_endpoint`
- `token_endpoint`
- `userinfo_endpoint`
- `scopes`

#### Provider Configuration (Stored in Database)
```yaml
google:
  enabled: true
  client_id: "xxxx.apps.googleusercontent.com"
  authorization_url: "https://accounts.google.com/o/oauth2/auth"
  token_url: "https://oauth2.googleapis.com/token"
  userinfo_url: "https://www.googleapis.com/oauth2/v3/userinfo"
  scopes: ["openid", "email", "profile"]

microsoft:
  enabled: true
  client_id: "xxxx"
  authorization_url: "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
  token_url: "https://login.microsoftonline.com/common/oauth2/v2.0/token"
  userinfo_url: "https://graph.microsoft.com/v1.0/me"
  scopes: ["User.Read", "email", "openid"]

facebook:
  enabled: true
  client_id: "xxxx"
  authorization_url: "https://www.facebook.com/v18.0/dialog/oauth"
  token_url: "https://graph.facebook.com/v18.0/oauth/access_token"
  userinfo_url: "https://graph.facebook.com/me?fields=id,name,email"
  scopes: ["email", "public_profile"]
```

#### Account Linking Strategy
- On first social login: create new user account linked to provider
- On subsequent login: match by `provider_subject_id` → authenticate
- Email matching optional: if email exists in system, prompt to link accounts
- Multiple providers can be linked to the same user account

---

## 29. JWT Strategy

### Token Structure

**Access Token (JWT)**
```json
{
  "sub": "user-uuid",
  "email": "user@institution.edu",
  "roles": ["admin", "faculty"],
  "permissions": ["routine:create", "routine:publish"],
  "session_id": "session-uuid",
  "type": "access",
  "iat": 1718726400,
  "exp": 1718727300,
  "iss": "eduroutine-api",
  "aud": "eduroutine-client"
}
```

**Refresh Token (Opaque)**
- Format: Random 64-byte value (base64url encoded)
- Stored: SHA-256 hash in Redis with user association
- Not a JWT — opaque for security

### Token Lifecycle
| Token | Lifetime | Storage | Rotation |
|---|---|---|---|
| Access Token | 15 minutes | Client (memory/session) | On refresh |
| Refresh Token | 7 days | Redis (hashed) | On use (rotation) |

### JWT Signing
- **Algorithm**: RS256 (RSA Signature with SHA-256)
- **Key Pair**: Generated at deployment, rotated quarterly
  - Private key: Server-side only, encrypted
  - Public key: Exposed at `/.well-known/jwks.json`
- **kid** (Key ID) header included for key rotation support

### JWT Validation Pipeline
```
1. Extract token from Authorization header
2. Validate signature (RS256 with JWKS)
3. Check expiry (exp claim)
4. Validate audience (aud claim)
5. Validate issuer (iss claim)
6. Check token not blacklisted (Redis)
7. Extract claims → set current user context
```

### Token Blacklisting
- On logout: add `jti` to Redis blacklist (TTL = token expiry)
- On password change: invalidate all user tokens
- On account lock/disable: immediate invalidation

---

## 30. Refresh Token Strategy

### Refresh Flow
```
1. POST /auth/refresh
   Body: { "refresh_token": "xxx" }

2. Server:
   a. Hash received refresh token
   b. Look up hash in Redis → get user_id + session_id
   c. Verify not revoked
   d. Issue new access token (15min) + new refresh token (7 days)
   e. Revolve old refresh token (rotation)
   f. Return new tokens

3. Response:
   {
     "access_token": "new-jwt",
     "refresh_token": "new-opaque",
     "token_type": "Bearer",
     "expires_in": 900
   }
```

### Refresh Token Rotation
- Every refresh operation issues a **new** refresh token
- Previous refresh token is immediately revoked
- If a revoked refresh token is reused → potential token theft detected → invalidate all user sessions

### Refresh Token Storage (Redis)
```
Key: rt:{sha256_hash}
Value: {
  "user_id": "uuid",
  "session_id": "uuid",
  "device_info": "Mozilla/5.0...",
  "ip_address": "192.168.1.1",
  "created_at": "2026-06-18T10:00:00Z"
}
TTL: 7 days (matches token expiry)
```

---

## 31. Social Login Design

### Implementation Strategy

#### Step 1: Initiate OAuth2
```
GET /api/v1/auth/oauth/{provider}
    ?redirect_uri=https://app.eduroutine.com/auth/callback
    &state=anti-csrf-token

Response: 302 Redirect to provider's authorization URL
```

#### Step 2: Provider Callback
```
GET /api/v1/auth/oauth/{provider}/callback
    ?code=authorization-code
    &state=anti-csrf-token

Server:
1. Validate state parameter matches stored CSRF token
2. Exchange authorization code for tokens (server-side)
3. Fetch user info from provider's userinfo endpoint
4. Look up or create user account
5. Link provider identity to user account
6. Issue access + refresh tokens
7. Redirect to frontend with tokens (fragment)
```

#### Step 3: Frontend Completes Auth
```
302 Redirect → eduroutine://auth/callback#access_token=xxx&refresh_token=xxx
```

### Social Login Database Schema

#### identity.external_logins
| Column | Type | Description |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK → users.id |
| provider | VARCHAR(50) | "google", "microsoft", "facebook" |
| provider_subject_id | VARCHAR(255) | Unique ID from provider |
| provider_email | VARCHAR(255) | Email from provider |
| raw_user_info | JSONB | Full provider response |
| linked_at | TIMESTAMPTZ | When account was linked |
| last_login_at | TIMESTAMPTZ | Last login timestamp |

### Account Linking Rules
1. If `provider_subject_id` exists → authenticate (login)
2. If `provider_email` matches existing user → prompt to link (first time)
3. No match → create new user account with email verified
4. Linked accounts can login via any linked provider or email/password

### Security Considerations
- PKCE required for mobile/SPA clients (no client secret)
- State parameter must be cryptographically random (CSRF protection)
- All provider communication over TLS 1.3
- Provider tokens never exposed to client
- Rate limit on failed OAuth attempts
- Periodic validation of provider JWKS keys
