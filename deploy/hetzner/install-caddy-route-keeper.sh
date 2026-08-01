#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
INSTALL_ROOT="${INSTALL_ROOT:-/}"

install -d "${INSTALL_ROOT}usr/local/lib/brightbean"
install -d "${INSTALL_ROOT}usr/local/sbin"
install -d "${INSTALL_ROOT}etc/systemd/system"
install -m 0755 "$ROOT/deploy/hetzner/ensure_brightbean_route.py" \
  "${INSTALL_ROOT}usr/local/lib/brightbean/ensure_brightbean_route.py"
install -m 0755 "$ROOT/deploy/hetzner/brightbean-caddy-route-keeper.sh" \
  "${INSTALL_ROOT}usr/local/sbin/brightbean-caddy-route-keeper"
install -m 0644 "$ROOT/deploy/hetzner/systemd/brightbean-caddy-route.service" \
  "${INSTALL_ROOT}etc/systemd/system/brightbean-caddy-route.service"
install -m 0644 "$ROOT/deploy/hetzner/systemd/brightbean-caddy-route.path" \
  "${INSTALL_ROOT}etc/systemd/system/brightbean-caddy-route.path"
install -m 0644 "$ROOT/deploy/hetzner/systemd/brightbean-caddy-route.timer" \
  "${INSTALL_ROOT}etc/systemd/system/brightbean-caddy-route.timer"

if [[ "$INSTALL_ROOT" != "/" ]]; then
  exit 0
fi

systemctl daemon-reload
systemctl enable --now brightbean-caddy-route.path brightbean-caddy-route.timer
systemctl start brightbean-caddy-route.service
