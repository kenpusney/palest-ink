# Palest Ink

> The palest ink is better than the best memory.  
> 好记性不如烂笔头。

[中文](./README.zh.md)

A memoryless document architecture for AI agents. Instead of relying on
implicit, auto-accumulating memory systems, Palest Ink replaces them with
explicit, user-declared project documents organized into four layers.

## Why

Agent memory systems — daily logs, MEMORY.md, cloud profiles, conversation
search — share the same fatal flaws:

- **Silent drift.** Information goes stale without warning. You cannot tell
  what the agent still believes versus what is outdated.
- **Context pollution.** Every session loads accumulated memory, whether
  relevant or not, wasting context window and diluting focus.
- **No inspection.** Memory is hidden state. You can't open a file and read
  what the agent remembers, verify its accuracy, or delete what's wrong.
- **Agent-only value.** Memory files serve the agent. They don't help
  collaborators, onboard new team members, or survive tool migration.

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

1. Copy `assets/INK.md` to your project root (or `.agents/INK.md`).
2. Fill in files and directories under each of the four layers.
3. The agent reads INK.md at session start and follows the paths.
4. The agent writes discoveries to the appropriate layer and session
   summaries to operational paths at session end.
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
| Hidden, uninspectable state | Open, readable files |
| Accumulates indefinitely | Curated and prunable |
| Agent-only value | Human + agent value |
| Context window bloat | Progressive disclosure |
| Drifts silently | Explicitly maintained |
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
