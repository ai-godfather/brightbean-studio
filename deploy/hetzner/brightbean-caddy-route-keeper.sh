#!/usr/bin/env bash
set -euo pipefail

SHOPAUTH_ROOT="${SHOPAUTH_ROOT:-/opt/shopauth}"
CADDYFILE="${SHOPAUTH_CADDYFILE:-${SHOPAUTH_ROOT}/infra/production/Caddyfile}"
HELPER="${BRIGHTBEAN_ROUTE_HELPER:-/usr/local/lib/brightbean/ensure_brightbean_route.py}"
COMPOSE_FILE="${SHOPAUTH_COMPOSE_FILE:-${SHOPAUTH_ROOT}/docker-compose.production.yml}"
ENV_FILE="${SHOPAUTH_ENV_FILE:-${SHOPAUTH_ROOT}/.env.production}"
BACKUP_DIR="${BRIGHTBEAN_ROUTE_BACKUP_DIR:-/var/backups/brightbean-caddy}"

for required in "$CADDYFILE" "$HELPER" "$COMPOSE_FILE" "$ENV_FILE"; do
  [[ -f "$required" ]] || { echo "[brightbean-route] missing $required" >&2; exit 1; }
done

set +e
check_output="$(python3 "$HELPER" --caddyfile "$CADDYFILE" 2>&1)"
check_status=$?
set -e
if [[ "$check_status" -eq 0 && "$check_output" == "unchanged" ]]; then
  exit 0
fi
if [[ "$check_status" -ne 2 || "$check_output" != "repair-required" ]]; then
  echo "[brightbean-route] preflight failed: $check_output" >&2
  exit 1
fi

candidate="$(mktemp "${CADDYFILE}.brightbean.XXXXXX")"
trap 'rm -f "$candidate"' EXIT
cp "$CADDYFILE" "$candidate"
python3 "$HELPER" --caddyfile "$candidate" --apply >/dev/null

docker run --rm \
  -v "$candidate:/etc/caddy/Caddyfile:ro" \
  --network shopauth-production_default \
  caddy:2.9-alpine caddy validate --config /etc/caddy/Caddyfile >/dev/null

mkdir -p "$BACKUP_DIR"
backup="${BACKUP_DIR}/Caddyfile.$(date -u +%Y%m%dT%H%M%SZ)"
cp "$CADDYFILE" "$backup"
install -m 0644 "$candidate" "$CADDYFILE"

cd "$SHOPAUTH_ROOT"
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" \
  up -d --no-deps --force-recreate caddy >/dev/null

echo "[brightbean-route] restored; backup=$backup"
