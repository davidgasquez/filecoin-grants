---
name: querying-oso
description: Queries Open Source Observer (OSO) for metrics, funding history and code activity on Filecoin projects, through OSO's MCP server or the pyoso Python client. Use when a FilPGF review or report needs measured numbers over time, or when a task mentions OSO or oso.xyz.
---

# Querying OSO

OSO is a SQL warehouse (Trino dialect) of open source and on-chain metrics. FilPGF uses it for the time series behind Kernel readings and for project activity.

## Connect

Pick the first that works:

1. **MCP**: the bundle registers OSO's server at `https://mcp.oso.xyz/mcp`. Sign in with OAuth when the client asks.
2. **pyoso**: create a free key at https://www.oso.xyz, then:

```bash
pip install pyoso
export OSO_API_KEY=...
```

```python
import os
from pyoso import Client

client = Client(api_key=os.environ["OSO_API_KEY"])
print(client.to_pandas("SELECT 1 AS ok"))
```

## Find the right table

Table names change; look them up rather than guessing:

```sql
SHOW SCHEMAS;
SHOW TABLES FROM metrics;
DESCRIBE <schema>.<table>;
```

The data catalog and model docs are at https://docs.oso.xyz. Always add a `LIMIT`.

## Linking to Karma

A Kernel project from reading-karma-data carries `osoProjectSlug`; filter OSO tables by that slug.

## Private data

Some FilPGF tables are shared only with the PLFIF organization on OSO. If a query fails with a permission error, say the data is PLFIF-only and carry on with public sources.
