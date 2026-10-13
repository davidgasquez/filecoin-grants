---
name: filpgf-read-karma
description: Reads public FilPGF data from the Karma API with a stdlib Python script — programs, funding applications and their criteria, project grants and milestones, the milestone verification queue, and Kernel functions, commitments and readings. No API key needed. Use when a task needs FilPGF or app.filpgf.io application, milestone, grant or Kernel data.
license: MIT
---

# Reading Karma data

app.filpgf.io is Karma's app for the `filecoin` community. Every read used here is a public GET on `https://gapapi.karmahq.xyz`; no key or sign-in.

Run the script from this skill's folder; it prints JSON:

```bash
python3 scripts/karma.py programs                 # program IDs and titles
python3 scripts/karma.py pending                  # milestones awaiting verification
python3 scripts/karma.py applications 1479        # every application to a program
python3 scripts/karma.py application APP-XXXX-XXXX
python3 scripts/karma.py grants <projectUID>      # grants with milestones
python3 scripts/karma.py project <projectUID>
python3 scripts/karma.py indicators <projectUID>  # Kernel indicators and readings
python3 scripts/karma.py kernel overview          # also: functions, projects, commitments
python3 scripts/karma.py get /v2/...              # any other GET
```

Pipe into `jq` or Python to filter. The script pages through lists for you.

## How the records connect

- An application (`referenceNumber`, e.g. `APP-…`) carries the form answers in `applicationData`, including the criteria a milestone is judged against. It links to a project through `projectUID`.
- A project has grants; each grant has `milestones` with `currentStatus`, `endsAt` and `statusHistory`.
- `pending` lists milestones the team marked complete that no reviewer has verified yet, with `projectUid` and `grantUid` to follow.
- Kernel `projects` and `commitments` key on `projectUID`; `functions` lists every Kernel function with its tier and SLA.

## Writing

Reads only. To apply, post updates or verify milestones, use Karma's skills: https://github.com/show-karma/skills
