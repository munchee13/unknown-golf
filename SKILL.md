---
name: unknown-golf
description: Use the official Unknown Golf REST API with full OpenAPI operation mapping. Trigger for Unknown Golf API tasks, including auth checks, endpoint discovery, event/community/player operations, tee updates, and direct operationId-based calls.
---

# Unknown Golf

Use this skill for official Unknown Golf API work.

## Quick start (60 seconds)

1) Validate auth:

```bash
python3 skills/unknown-golf/scripts/unknown_golf_api.py auth-test
```

2) List operations:

```bash
python3 skills/unknown-golf/scripts/unknown_golf_api.py list-operations
```

3) Call an operation by `operationId`:

```bash
python3 skills/unknown-golf/scripts/unknown_golf_api.py call \
  --operation-id search_1 \
  --body '{"communityId":705}'
```

## Rules

- Use official API endpoints only (`https://api.unknowngolf.com`).
- Use OpenAPI mapping from `references/openapi.json` and `references/openapi.yaml`.
- Authenticate with `POST /v1/auth` and Bearer token.
- Normalize plain numeric single-round event IDs to `S-<id>` when needed.

## What this API can do (practical)

- Search events/players/teams/scores.
- Add or remove event players.
- Update player tee assignments for events.
- Manage teams (create, delete, assign/remove players).
- Manage flights (list, assign/remove players/teams, delete).
- Manage tee pairings (create, update, assign/remove players, delete).
- Read event leaderboard metadata and related flight/unassigned views.
- Generate/share event web links (results, tee sheet, scoring, registration).

## Known limitations

- The documented public API does not expose full event deletion.
- Do not assume `DELETE /v1/events/{eventId}` is supported for full removal.
- For full event deletion, use the league UI delete flow.
- Leaderboards are readable, but full leaderboard-definition CRUD is not documented.
- Event primary course switching is not exposed as a documented public API operation.

## Common recipes

### 1) List players in an event

```bash
python3 skills/unknown-golf/scripts/unknown_golf_api.py event-players list --event-id 115986
```

### 2) Add a known playerId to an event

```bash
python3 skills/unknown-golf/scripts/unknown_golf_api.py event-players add-ids --event-id 115986 --player-id 81374
```

### 3) Set a player's tee in an event

```bash
python3 skills/unknown-golf/scripts/unknown_golf_api.py call \
  --operation-id updateTee \
  --path-params '{"eventId":"S-115986","playerId":81374,"teeId":107849}'
```

### 4) Raw call when you already know method/path

```bash
python3 skills/unknown-golf/scripts/unknown_golf_api.py raw \
  --method GET \
  --path /v1/events/S-115986/players
```

## Script reference

Use `scripts/unknown_golf_api.py`.

### Helpful commands

```bash
# Auth check
python3 skills/unknown-golf/scripts/unknown_golf_api.py auth-test

# Explore API
python3 skills/unknown-golf/scripts/unknown_golf_api.py list-operations
python3 skills/unknown-golf/scripts/unknown_golf_api.py list-operations --tag Event
python3 skills/unknown-golf/scripts/unknown_golf_api.py list-operations --contains players

# Call by operationId
python3 skills/unknown-golf/scripts/unknown_golf_api.py call --operation-id search_4 --path-params '{"eventId":"S-115986"}'
```

## Credentials

The script uses one of these, in order:

1. Env vars: `UG_API_EMAIL`, `UG_API_PASSWORD`
2. macOS keychain services: `unknowngolf-username`, `unknowngolf-password`

Optional base override:

- `UG_API_BASE` (defaults to `https://api.unknowngolf.com`)

## Troubleshooting

- `401 Unauthorized`: verify credentials and rerun `auth-test`.
- Empty/`204` response: query succeeded but no matching records.
- Event not found: try `S-<id>` format (for example `S-115986`).
- Delete event failed: expected for public API, use UI delete flow.

## Shareability

This skill is safe to share.

- No credentials are embedded.
- Receivers must supply their own API credentials or keychain entries.
