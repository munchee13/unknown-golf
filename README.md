# unknown-golf

OpenClaw skill for the official Unknown Golf REST API.

## Includes

- `SKILL.md` usage guide
- `scripts/unknown_golf_api.py` unified CLI
- `references/openapi.yaml` and `references/openapi.json`
- `references/operation-map.md`

## Notes

- Uses documented public API endpoints.
- Full event deletion is not exposed in documented public API (use UI delete flow).
- No credentials are stored in this repo.

## Auth (local)

Use either:
- `UG_API_EMAIL` + `UG_API_PASSWORD` env vars, or
- macOS keychain entries: `unknowngolf-username`, `unknowngolf-password`
