# Eval 2: Selective Load - With Skill

## Whether I read INK.md

Yes. I read `/tmp/palest-ink-eval/eval-2-selective-load/project/INK.md` as the first step, following the palest-ink skill's instruction: "On session start, read INK.md."

## Which documents I loaded

Based on the user's question ("API 认证是怎么实现的？"), I classified it as a "how" question (behavioral) with architectural relevance (conceptual). I loaded:

1. **docs/conceptual/architecture.md** -- loaded because authentication is an architectural decision, and this document answers "why" and "how" at a design level. This is where the key answer was found.
2. **docs/behavioral/coding-standards.md** -- loaded because it is the behavioral layer document, and authentication conventions might be recorded there.

## Which documents I intentionally did NOT load

1. **docs/operational/changelog.md** -- skipped because it records "what happened" (logs, changelogs), which is not relevant to understanding how API authentication is implemented.
2. **docs/structural/** -- skipped because the directory is empty (no files present).

## Answer to the user's question

This project uses a JWT + Refresh Token dual-token authentication mechanism:

- **Access Token**: expires in 15 minutes, stored in memory.
- **Refresh Token**: expires in 7 days, stored in an HttpOnly Cookie.
- **Refresh logic**: when the Access Token expires, the Refresh Token is used to obtain a new one. When the Refresh Token expires, the user is redirected to the login page.

The overall architecture is a front-end/back-end separation with Next.js on the frontend and Express + PostgreSQL on the backend. The database uses Prisma ORM with core tables including users, projects, tasks, and audit_logs.

## Whether I wrote anything back to any document

No. I did not write anything back to any document. The task was purely a read/answer task with no operational work performed, and no new discoveries that should be persisted.
