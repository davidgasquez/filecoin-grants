---
name: querying-oso
description: Queries Open Source Observer (OSO) for metrics, funding history and code activity on Filecoin projects through OSO's MCP server. Use when a FilPGF review or report needs measured numbers over time, or when a task mentions OSO or oso.xyz.
---

# Querying OSO

OSO is a SQL warehouse (Trino dialect) of open source and on-chain metrics. FilPGF uses it for the time series behind Kernel readings and for project activity.

## Connect

This bundle registers OSO's MCP server as `oso` at `https://mcp.oso.xyz/mcp`. Sign in with OAuth (a free oso.xyz account) when the client asks. Agents that don't install the bundle add that URL as a remote MCP server by hand.

## Query

Copy this checklist:

```
OSO query:
- [ ] 1. Get the org id
- [ ] 2. Find the table and its columns
- [ ] 3. Submit the SQL
- [ ] 4. Poll for the result
```

1. **Org id**: `oso:GetViewer` lists your organizations. Every query tool takes one `orgId`.
2. **Table**: `oso:ListDatasets` lists the datasets you can read; `oso:ListTablesForDataset` (with `datasetName`, e.g. `metrics`) lists each table's full name and columns. Page with `after` while `pageInfo.hasNextPage` is true. Look tables up this way rather than guessing names; `SHOW TABLES` is not permitted.
3. **Submit**: `oso:SqlQuery` with `orgId` and the SQL, using each table's `fullName`. Always add a `LIMIT`. It returns a `runId`, not rows.
4. **Poll**: `oso:GetAsyncQueryResult` with `orgId` and `runId` until `status` is no longer `QUEUED` or `RUNNING`. A `FAILED` run explains why in `message`. Raise `rowLimit` (up to 1000) if `truncated` is true.

## Linking to Karma

A Kernel project from reading-karma-data carries `osoProjectSlug`; filter OSO tables by that slug.

## Private data

Some FilPGF tables are shared only with the PLFIF organization on OSO. A `PERMISSION_DENIED` failure means the data isn't shared with you: say it's PLFIF-only and carry on with public sources.
