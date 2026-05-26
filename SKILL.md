---
name: palest-ink
description: "A memoryless document architecture."
license: MIT
metadata:
  author: kenpusney
  version: "0.1.0"
---

# Palest Ink

The palest ink is better than the best memory. 好记性不如烂笔头。

Disable all implicit memory systems — MEMORY.md, .workbuddy/memory/,
conversation_search. Classify project documents into four layers:
conceptual, structural, behavioral, operational. Store path mappings in
INK.md at the project root or under .agents/. See assets/INK.md for the
default template. On first use, copy it into place. Seek user approval
before any change to INK.md.

At session start, read INK.md and load only documents relevant to the
current task. When new information is discovered, write it to the
appropriate layer's paths. At session end, write to operational paths.
