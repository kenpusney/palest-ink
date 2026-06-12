# Eval Summary: Selective Load - API Authentication

## Read INK.md

Yes. I read the INK.md file at `/tmp/palest-ink-eval/eval-2-selective-load/project/INK.md` to understand the document layer structure before proceeding.

## Documents Loaded

1. **docs/conceptual/architecture.md** -- Loaded. This was the primary relevant document for answering the API authentication question. It directly describes the auth scheme.
2. **docs/behavioral/coding-standards.md** -- Loaded. Checked for any auth-related coding conventions. Contains general TypeScript, Git, and testing standards but nothing specific to authentication.
3. **docs/operational/changelog.md** -- Loaded. Checked for recent auth-related changes. Contains pagination fixes and Next.js upgrades, no auth entries.
4. **docs/structural/** -- Checked but intentionally NOT loaded. The directory was empty; INK.md referenced it as a directory path without a specific file.

## Answer to the User's Question

The project uses a **JWT + Refresh Token dual-token mechanism** for API authentication:

- **Access Token**: 15-minute expiry, stored in memory.
- **Refresh Token**: 7-day expiry, stored in an HttpOnly Cookie.
- **Refresh logic**: When the Access Token expires, the Refresh Token is used to obtain a new one. When the Refresh Token expires, the user is redirected to the login page.

The backend is Express with PostgreSQL (via Prisma ORM). Core tables include `users`, `projects`, `tasks`, and `audit_logs`.

## Searched Across Documents Using Grep/Glob

No. I did not use Grep or Glob. Since the project had only 3 documents and an empty structural directory, I read each file directly. The document set was small enough that targeted reads against the INK.md index were sufficient without keyword searching.
