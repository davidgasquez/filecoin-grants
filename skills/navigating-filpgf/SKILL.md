---
name: navigating-filpgf
description: Orients an agent in Filecoin Public Goods Funding (FilPGF) — the Kernel, Revenue Development and R&D programs, ProPGF batches, and where each kind of data lives (filpgf.io, app.filpgf.io on Karma, OSO). Use when a task mentions FilPGF, filpgf.io, Kernel, ProPGF, PLFIF, or Filecoin grants, before picking a data or review skill.
---

# Navigating FilPGF

filpgf.io is the public site for Filecoin's public goods funding. Applications, milestones, reports and payouts live in app.filpgf.io, which runs on Karma. Read the site for what each program funds; read the data from its source, never from the site copy.

## Programs

Each program's page is its source of truth for scope, terms and how to get in:

- Kernel — infrastructure the network can't run without: https://www.filpgf.io/kernel/
- Revenue Development — growth, run as pods: https://www.filpgf.io/revenue-development/
- R&D — request-driven early work: https://www.filpgf.io/rnd/
- ProPGF — the milestone-based funding rounds: https://www.filpgf.io/propgf/

For a one-file overview of every page, fetch https://www.filpgf.io/llms.txt.

## Where each kind of data lives

| Data | Source | Skill |
|---|---|---|
| Applications, criteria, approved amounts | Karma funding applications | reading-karma-data |
| Grants, milestones, verification queue | Karma projects and grants | reading-karma-data |
| Kernel functions, commitments, readings | Karma `/v2/kernel/*` | reading-karma-data |
| Metrics, funding history, code activity | OSO | querying-oso |
| Code | the project's git repository | clone it |

When two sources disagree, Karma wins for amounts and milestone status, OSO for metrics and git for code. Show both values rather than picking one silently.

For Karma program IDs, run the `programs` command from reading-karma-data.

## Reviewing work

For a milestone or project review, use reviewing-kernel-work.

## Writing to Karma

Applying, posting milestones or verifying them needs a Karma account and role. Use Karma's own skills for that: https://github.com/show-karma/skills
