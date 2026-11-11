# project-baseline Specification

## ADDED Requirements

### Requirement: Project structure
The project SHALL maintain upstream Project NOMAD structure with Hyper extensions.

#### Scenario: Baseline
- WHEN a developer clones the repo
- THEN they find upstream code + docs/hyper + brain/ + openspec/ + agents/ + .claude/skills

### Requirement: Documentation
The project SHALL provide multi-language documentation under docs/.

#### Scenario: Locales
- WHEN docs are built
- THEN at least EN and RU are complete
