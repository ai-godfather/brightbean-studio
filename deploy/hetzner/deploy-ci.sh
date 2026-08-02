#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SERVER_IP="${PROD_SERVER_IP:?set PROD_SERVER_IP}"
SSH_USER="${PROD_SSH_USER:-root}"
TARGET="${BRIGHTBEAN_TARGET:-/opt/brightbean-studio}"
COMPOSE_FILE="deploy/hetzner/docker-compose.yml"
ENV_FILE="deploy/hetzner/.env"
DEPLOY_REVISION="${GITHUB_SHA:-$(git -C "$ROOT" rev-parse HEAD)}"
COMPOSE_BUILD="${COMPOSE_BUILD:-1}"

ssh_target="${SSH_USER}@${SERVER_IP}"
ssh_options=(
  -o BatchMode=yes
  -o ConnectTimeout=10
  -o StrictHostKeyChecking=accept-new
)

echo "[brightbean-deploy] target=${SSH_USER}@server:${TARGET} revision=${DEPLOY_REVISION}"

for attempt in $(seq 1 12); do
  if ssh "${ssh_options[@]}" "$ssh_target" "echo ready" >/dev/null 2>&1; then
    break
  fi
  if [[ "$attempt" -eq 12 ]]; then
    echo "[brightbean-deploy] SSH is unreachable" >&2
    exit 1
  fi
  sleep 5
done

ssh "${ssh_options[@]}" "$ssh_target" "mkdir -p '$TARGET'"

rsync -az --delete --delete-excluded \
  -e "ssh ${ssh_options[*]}" \
  --filter "protect ${ENV_FILE}" \
  --filter "protect .deploy-revision" \
  --filter "protect .deploy-attempt" \
  --exclude '.git/' \
  --exclude '.env' \
  --exclude '.env.*' \
  --exclude 'deploy/hetzner/.env' \
  --exclude '.venv/' \
  --exclude '__pycache__/' \
  --exclude '.pytest_cache/' \
  --exclude '.mypy_cache/' \
  --exclude '.ruff_cache/' \
  "$ROOT/" "$ssh_target:$TARGET/"

ssh "${ssh_options[@]}" "$ssh_target" \
  "test -s '$TARGET/$ENV_FILE' || { echo 'Missing $TARGET/$ENV_FILE' >&2; exit 1; }"

ssh "${ssh_options[@]}" "$ssh_target" \
  "chmod +x '$TARGET/deploy/hetzner/'*.sh '$TARGET/deploy/hetzner/ensure_brightbean_route.py' && printf '%s\n' '$DEPLOY_REVISION' > '$TARGET/.deploy-attempt'"

remote_compose="docker compose --env-file '$TARGET/$ENV_FILE' -f '$TARGET/$COMPOSE_FILE'"

ssh "${ssh_options[@]}" "$ssh_target" "$remote_compose config --quiet"

if [[ "$COMPOSE_BUILD" == "1" ]]; then
  ssh "${ssh_options[@]}" "$ssh_target" "$remote_compose build app"
fi

# The one-shot migrate service is a dependency of app and worker. Compose will
# fail closed if the migration cannot complete, before either service changes.
ssh "${ssh_options[@]}" "$ssh_target" "$remote_compose up -d"

# Public ingress is shared because the VPS has one public 80/443 listener, but
# the route source, reconciliation code and systemd ownership live here.
ssh "${ssh_options[@]}" "$ssh_target" \
  "'$TARGET/deploy/hetzner/install-caddy-route-keeper.sh'"

ssh "${ssh_options[@]}" "$ssh_target" \
  "$remote_compose ps && test \"\$(docker inspect -f '{{.State.Health.Status}}' brightbean-production-app-1)\" = healthy"

curl --fail --silent --show-error --location --max-time 30 \
  "https://studio.shopauth.cloud/health/" >/dev/null

ssh "${ssh_options[@]}" "$ssh_target" \
  "printf '%s\n' '$DEPLOY_REVISION' > '$TARGET/.deploy-revision'"

echo "[brightbean-deploy] completed revision=${DEPLOY_REVISION}"
