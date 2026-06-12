# Palest Ink

> The palest ink is better than the strongest memory.  
> 好记性不如烂笔头。

[中文](./README.zh.md)

A memoryless document architecture for AI agents. Instead of relying on
implicit, auto-accumulating memory systems, Palest Ink replaces them with
explicit, user-declared project documents organized into four layers.

## Why

Implicit memory systems — Mem0, MemPalace, auto-summarizing MEMORY files,
vector-database-backed memory plugins — share the same fatal flaws:

- **Uncontrollable accumulation.** Auto-summarizing systems keep organizing
  and rewriting memory on their own, so you can never be sure what's in
  there, whether it's still relevant, or whether it should exist at all.
- **Opaque storage.** Memories live in vector databases or compressed
  summaries you can't directly read, edit, or verify.
- **Size limits force lossy compression.** Memory systems have token or
  storage caps. When they fill up, old information is silently dropped or
  merged — you don't know what was lost.
- **Agent-only value.** Memory is structured for the agent, not for humans.
  It doesn't help collaborators, onboard new team members, or survive
  tool migration.

Documents fix all of this. A document is inspectable, editable, deletable,
version-controllable, and useful to humans as well as agents.

## Principles

**Explicit over implicit.** Every piece of knowledge lives in a named file
at a known path, declared by you. Nothing is hidden.

**User owns the map.** The agent follows your INK.md — it does not decide
where things go. Any change to the map requires your approval.

**Progressive disclosure.** The agent reads only what the current task needs,
not a dump of everything it has ever known.

**Freshness over completeness.** Stale information is worse than none. Keep
documents current or delete them.

## Four-Layer Taxonomy

| Layer | Question | Typical Content |
|-------|----------|-----------------|
| Conceptual | Why | Vision, design decisions, constraints, anti-goals, domain model |
| Structural | Where | File layout, module graph, data schemas, content organization |
| Behavioral | How | Conventions, workflows, rules, style guides, checklists |
| Operational | What happened | Session logs, changelogs, task records, debugging notes |

The taxonomy is universal. It applies equally to software projects, fiction
manuscripts, research work, product planning — any project with purpose,
structure, process, and history.

## Usage

```bash
npx skills@latest add kenpusney/palest-ink
```

1. Copy `skills/palest-ink/assets/INK.md` to your project root (or `.agents/INK.md`).
2. Fill in files and directories under each of the four layers.
3. The agent reads INK.md at session start and follows the paths.
4. The agent writes discoveries to the appropriate layer. Operational
   entries are written whenever operational work is done.
5. You can change INK.md at any time. The agent cannot without your approval.

### Example INK.md

```markdown
# INK.md

## Conceptual
- docs/conceptual/design-principles.md
- docs/conceptual/adr/
- docs/conceptual/domain-reference.md

## Structural
- docs/structural/architecture.md
- docs/structural/module-map.md
- docs/structural/data-models.md

## Behavioral
- docs/behavioral/coding-standards.md
- docs/behavioral/project-rules.md
- docs/behavioral/api-contracts.md

## Operational
- docs/operational/changelog.md
- docs/operational/sessions/
- docs/operational/debugging-notes.md
```

You can also point to individual files instead of directories, or mix both.
There is no prescribed layout — INK.md reflects your project, not a template.

## Advantages Over Automatic Memory

| Automatic Memory | Palest Ink |
|---|---|
| Opaque (vector DB, compressed summaries) | Open, readable plain text files |
| Auto-accumulates, hard to control | Curated by the user, prunable |
| Size limits force lossy compression | No size limits, files grow as needed |
| Agent-only value | Human + agent value |
| Tied to tool/platform | Portable, plain text |

## Limitations

- **Cold start cost.** A fresh project has no documents. The first session
  with Palest Ink requires bootstrapping INK.md and initial documents.
- **Discipline required.** The agent writes to documents, but the human owns
  pruning. Neglected documents become the very cruft this architecture
  was designed to avoid.
- **Not a knowledge base.** Palest Ink organizes project knowledge — it does
  not replace wikis, Notion, or long-form documentation for external audiences.
- **Agent judgment varies.** Taxonomy classification depends on the agent's
  understanding. Review INK.md mappings periodically.

## Recommendations

- Start small. Map what you already have. Don't create documents for the
  sake of filling layers.
- Review operational logs monthly. Archive or delete anything older than
  30 days that provides no ongoing value.
- Treat INK.md as living documentation. Update it when your project
  structure changes.
- For team projects, commit INK.md and referenced documents to version control.
