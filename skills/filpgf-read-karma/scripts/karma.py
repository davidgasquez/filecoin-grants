#!/usr/bin/env python3
"""Read public FilPGF data from the Karma API. Stdlib only, no key needed.

Usage: python3 scripts/karma.py <command> [args]

  programs                     Filecoin programs on Karma (id, title)
  pending                      Milestones marked complete, awaiting verification
  applications PROGRAM_ID      All applications to a program
  application REF              One application, e.g. APP-QQ7MMWRN-QJJGQS
  project PROJECT_UID          Project details
  grants PROJECT_UID           A project's grants, with milestones
  indicators PROJECT_UID       A project's Kernel indicators and readings
  kernel overview|functions|projects|commitments
  get /v2/PATH                 Any other GET, printed as-is

Prints JSON to stdout. Set KARMA_API_ORIGIN to point at another indexer.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ORIGIN = os.environ.get("KARMA_API_ORIGIN", "https://gapapi.karmahq.xyz").rstrip("/")
COMMUNITY = "filecoin"
# The API caps list pages at 50 items, whatever limit is asked for.
PAGE_SIZE = 50
# The indexer answers in under a few seconds; 30s leaves room for slow links.
TIMEOUT = 30
# The same window the filpgf.io Kernel page uses for its readings.
KERNEL_WINDOW_DAYS = 30


def get(path, **params):
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{ORIGIN}{path}" + (f"?{query}" if query else "")
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        sys.exit(f"GET {url} failed: HTTP {error.code}. Check the id or reference.")
    except urllib.error.URLError as error:
        sys.exit(f"GET {url} failed: {error.reason}. Is the network reachable?")


def pending():
    items, page = [], 1
    while True:
        body = get(f"/v2/communities/{COMMUNITY}/milestones/pending-verification",
                   page=page, limit=PAGE_SIZE)
        items += body.get("data", [])
        info = body.get("pageInfo", {})
        if page * info.get("pageLimit", PAGE_SIZE) >= info.get("totalItems", 0):
            return items
        page += 1


def applications(program_id):
    items, page = [], 1
    while True:
        body = get(f"/v2/funding-applications/program/{program_id}",
                   page=page, limit=PAGE_SIZE)
        items += body.get("applications", [])
        if page >= body.get("pagination", {}).get("totalPages", 1):
            return items
        page += 1


def programs():
    return [
        {"programId": p["programId"], "title": p.get("metadata", {}).get("title")}
        for p in get(f"/v2/communities/{COMMUNITY}/programs")
    ]


def kernel(view):
    views = ("overview", "functions", "projects", "commitments")
    if view not in views:
        sys.exit(f"kernel view must be one of: {', '.join(views)}")
    window = None if view == "commitments" else KERNEL_WINDOW_DAYS
    return get(f"/v2/kernel/{view}", windowDays=window)


COMMANDS = {
    "programs": (0, programs),
    "pending": (0, pending),
    "applications": (1, applications),
    "application": (1, lambda ref: get(f"/v2/funding-applications/{ref}")),
    "project": (1, lambda uid: get(f"/v2/projects/{uid}")),
    "grants": (1, lambda uid: get(f"/v2/projects/{uid}/grants")),
    "indicators": (1, lambda uid: get(f"/v2/indicators/projects/{uid}")),
    "kernel": (1, kernel),
    "get": (1, lambda path: get(path if path.startswith("/") else f"/{path}")),
}


def main(argv):
    if not argv or argv[0] not in COMMANDS:
        sys.exit(__doc__)
    arity, command = COMMANDS[argv[0]]
    if len(argv) - 1 != arity:
        sys.exit(f"'{argv[0]}' takes {arity} argument(s).\n{__doc__}")
    json.dump(command(*argv[1:]), sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
