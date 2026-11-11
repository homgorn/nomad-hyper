---
id: openspec
title: OpenSpec SDD Workflow
summary: OpenSpec spec-driven development. Workflow: explore -> propose -> apply -> verify -> archive. Artifacts: proposal.md, specs/, design.md, tasks.md.
tags: [openspec, sdd, workflow]
entities: [OpenSpec, Fission AI]
claims: []
sources: [https://openspec.dev]
updated: 2026-11-11
---

# OpenSpec SDD Workflow

## Commands (OpenCode)
- /opsx-explore — explore idea
- /opsx-propose — draft proposal + specs + design + tasks
- /opsx-apply — implement tasks
- /opsx-verify — verify implementation matches spec
- /opsx-archive — archive completed change

## Structure
```
openspec/
├── config.yaml
├── specs/          # source of truth
├── changes/        # in-flight changes
└── changes/archive/ # completed
```

## First change
`/opsx-propose "hyper-v2 baseline: import hyperspec, modules, agent layer, docker v2 compose"`
