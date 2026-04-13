#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

API_BASE_DEFAULT = "https://api.unknowngolf.com"
SKILL_DIR = Path(__file__).resolve().parents[1]
OPENAPI_JSON = SKILL_DIR / "references" / "openapi.json"


class ApiError(RuntimeError):
    pass


def _keychain_get(service: str) -> Optional[str]:
    try:
        out = subprocess.check_output(
            ["security", "find-generic-password", "-s", service, "-w"],
            stderr=subprocess.DEVNULL,
            timeout=8,
        )
        return out.decode().strip()
    except Exception:
        return None


def _load_json_arg(raw: Optional[str], field: str) -> Dict[str, Any]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ApiError(f"Invalid JSON for {field}: {e}")
    if not isinstance(parsed, dict):
        raise ApiError(f"{field} must be a JSON object")
    return parsed


def load_openapi() -> Dict[str, Any]:
    if not OPENAPI_JSON.exists():
        raise ApiError(f"OpenAPI file missing: {OPENAPI_JSON}")
    with OPENAPI_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or "paths" not in data:
        raise ApiError("Invalid OpenAPI document")
    return data


def load_creds() -> Tuple[str, str]:
    email = os.getenv("UG_API_EMAIL") or _keychain_get("unknowngolf-username")
    password = os.getenv("UG_API_PASSWORD") or _keychain_get("unknowngolf-password")
    if not email or not password:
        raise ApiError(
            "Missing Unknown Golf credentials. Set UG_API_EMAIL/UG_API_PASSWORD or keychain items unknowngolf-username/unknowngolf-password."
        )
    return email, password


def auth_token(api_base: str) -> str:
    email, password = load_creds()
    payload = {"email": email, "password": password}
    out = http_json(api_base, "POST", "/v1/auth", body=payload, token=None)
    token = out.get("token") if isinstance(out, dict) else None
    if not token:
        raise ApiError("Auth succeeded but token missing in response")
    return token


def http_json(
    api_base: str,
    method: str,
    path: str,
    token: Optional[str],
    body: Optional[Dict[str, Any]] = None,
    query: Optional[Dict[str, Any]] = None,
) -> Any:
    if not path.startswith("/"):
        path = "/" + path
    url = api_base.rstrip("/") + path
    if query:
        pairs = []
        for k, v in query.items():
            if v is None:
                continue
            if isinstance(v, list):
                for item in v:
                    pairs.append((k, json.dumps(item) if isinstance(item, (dict, list)) else str(item)))
            else:
                pairs.append((k, json.dumps(v) if isinstance(v, (dict, list)) else str(v)))
        if pairs:
            url += "?" + urllib.parse.urlencode(pairs)

    payload = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=payload, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            if not raw.strip():
                return {"status": resp.status, "body": None}
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"status": resp.status, "body": raw}
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        raise ApiError(f"{method.upper()} {path} failed: HTTP {e.code} {detail}".strip())


def collect_operations(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    ops: List[Dict[str, Any]] = []
    for path, item in (doc.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        for method in ["get", "post", "put", "patch", "delete", "options", "head"]:
            op = item.get(method)
            if not isinstance(op, dict):
                continue
            ops.append(
                {
                    "operationId": op.get("operationId"),
                    "method": method.upper(),
                    "path": path,
                    "summary": op.get("summary", ""),
                    "tags": op.get("tags", []),
                    "hasRequestBody": "requestBody" in op,
                }
            )
    return ops


def find_operation(doc: Dict[str, Any], operation_id: str) -> Dict[str, Any]:
    matches: List[Dict[str, Any]] = []
    for op in collect_operations(doc):
        if op.get("operationId") == operation_id:
            matches.append(op)
    if not matches:
        raise ApiError(f"operationId not found: {operation_id}")
    if len(matches) > 1:
        raise ApiError(f"operationId is not unique: {operation_id}")
    return matches[0]


def apply_path_params(path_template: str, path_params: Dict[str, Any]) -> str:
    out = path_template
    for k, v in path_params.items():
        out = out.replace("{" + str(k) + "}", urllib.parse.quote(str(v), safe=""))
    if "{" in out and "}" in out:
        raise ApiError(f"Unresolved path params in path: {out}")
    return out


def cmd_auth_test(args: argparse.Namespace) -> None:
    token = auth_token(args.api_base)
    print(json.dumps({"ok": True, "tokenPrefix": token[:16] + "..."}, indent=2))


def cmd_list_operations(args: argparse.Namespace) -> None:
    doc = load_openapi()
    ops = collect_operations(doc)

    if args.tag:
        ops = [o for o in ops if args.tag in (o.get("tags") or [])]
    if args.contains:
        needle = args.contains.lower()
        ops = [
            o
            for o in ops
            if needle in (o.get("path", "").lower())
            or needle in (o.get("summary", "").lower())
            or needle in str(o.get("operationId", "")).lower()
        ]

    ops = sorted(ops, key=lambda x: (str(x.get("tags", [""])[0] if x.get("tags") else ""), x.get("path", ""), x.get("method", "")))
    print(json.dumps({"count": len(ops), "operations": ops}, indent=2))


def cmd_call(args: argparse.Namespace) -> None:
    doc = load_openapi()
    op = find_operation(doc, args.operation_id)

    path_params = _load_json_arg(args.path_params, "--path-params")
    query = _load_json_arg(args.query, "--query")
    body = _load_json_arg(args.body, "--body") if args.body else None

    path = apply_path_params(op["path"], path_params)
    token = auth_token(args.api_base)
    out = http_json(args.api_base, op["method"], path, token=token, body=body, query=query)
    print(
        json.dumps(
            {
                "operationId": op["operationId"],
                "method": op["method"],
                "path": path,
                "query": query,
                "response": out,
            },
            indent=2,
        )
    )


def cmd_raw(args: argparse.Namespace) -> None:
    query = _load_json_arg(args.query, "--query")
    body = _load_json_arg(args.body, "--body") if args.body else None
    token = auth_token(args.api_base)
    out = http_json(args.api_base, args.method, args.path, token=token, body=body, query=query)
    print(json.dumps({"method": args.method.upper(), "path": args.path, "response": out}, indent=2))


def cmd_event_players(args: argparse.Namespace) -> None:
    event_id = args.event_id.strip()
    if event_id.isdigit():
        event_id = f"S-{event_id}"
    token = auth_token(args.api_base)

    if args.event_cmd == "list":
        out = http_json(args.api_base, "GET", f"/v1/events/{event_id}/players", token=token)
        print(json.dumps({"eventId": event_id, "count": len(out) if isinstance(out, list) else None, "players": out}, indent=2))
        return

    if args.event_cmd == "add-ids":
        added, failed = [], []
        for pid in args.player_id:
            try:
                resp = http_json(
                    args.api_base,
                    "POST",
                    f"/v1/events/{event_id}/players",
                    token=token,
                    body={"playerId": int(pid)},
                )
                added.append(resp)
            except Exception as e:
                failed.append({"playerId": int(pid), "error": str(e)})
        players = http_json(args.api_base, "GET", f"/v1/events/{event_id}/players", token=token)
        print(json.dumps({"eventId": event_id, "added": added, "failed": failed, "finalCount": len(players) if isinstance(players, list) else None}, indent=2))
        return

    raise ApiError(f"Unsupported event command: {args.event_cmd}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Unknown Golf API CLI (OpenAPI-mapped)")
    p.add_argument("--api-base", default=os.getenv("UG_API_BASE", API_BASE_DEFAULT), help="API base URL")

    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("auth-test", help="Validate credentials and auth")
    s.set_defaults(func=cmd_auth_test)

    s = sub.add_parser("list-operations", help="List all mapped OpenAPI operations")
    s.add_argument("--tag", help="Filter by tag")
    s.add_argument("--contains", help="Filter by operationId/path/summary text")
    s.set_defaults(func=cmd_list_operations)

    s = sub.add_parser("call", help="Call an operation by operationId")
    s.add_argument("--operation-id", required=True, help="OpenAPI operationId")
    s.add_argument("--path-params", help='JSON object, e.g. {"eventId":"S-115986"}')
    s.add_argument("--query", help='JSON object for query params, e.g. {"page":1}')
    s.add_argument("--body", help='JSON object for request body')
    s.set_defaults(func=cmd_call)

    s = sub.add_parser("raw", help="Raw API call (method + path)")
    s.add_argument("--method", required=True, help="HTTP method")
    s.add_argument("--path", required=True, help="Path, e.g. /v1/events")
    s.add_argument("--query", help="JSON object for query params")
    s.add_argument("--body", help="JSON object for request body")
    s.set_defaults(func=cmd_raw)

    s = sub.add_parser("event-players", help="Convenience helper for event player operations")
    ev = s.add_subparsers(dest="event_cmd", required=True)

    e = ev.add_parser("list", help="List players in an event")
    e.add_argument("--event-id", required=True)
    e.set_defaults(func=cmd_event_players)

    e = ev.add_parser("add-ids", help="Register players by playerId")
    e.add_argument("--event-id", required=True)
    e.add_argument("--player-id", type=int, action="append", required=True)
    e.set_defaults(func=cmd_event_players)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except ApiError as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
