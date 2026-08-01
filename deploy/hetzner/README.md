# Hetzner deployment next to ShopAuth

This profile runs BrightBean as the independent Docker Compose project
`brightbean-production`. It does not expose PostgreSQL or bind host ports. Only
the `app` service joins ShopAuth's existing external network so the existing
Caddy container can reach the stable alias `brightbean-app:8000`.

## Prerequisites

- DNS `studio.shopauth.cloud` points to the ShopAuth Hetzner server.
- Docker network `shopauth-production_default` exists.
- A dedicated S3-compatible bucket exists for BrightBean media.
- `deploy/hetzner/.env` is created from `.env.example` and remains untracked.

Large video uploads over MCP require `STORAGE_BACKEND=s3`. The MCP flow is:

1. Call `request_media_upload`.
2. Submit the returned fields and binary file to the returned presigned URL.
3. Call `finalize_media_upload`.
4. Poll `get_media` until processing is complete.
5. For a Reel, call `create_draft` with `post_type: "reel"` and, when a
   custom cover is used, `cover_image_asset_id: "<completed-image-asset-id>"`.
   Both fields are persisted in `PlatformPost.platform_extra` and returned by
   `create_draft` / `get_post` for verification.
6. Review the draft and only then schedule the post.

## Deploy

```bash
docker compose --env-file deploy/hetzner/.env \
  -f deploy/hetzner/docker-compose.yml build app
docker compose --env-file deploy/hetzner/.env \
  -f deploy/hetzner/docker-compose.yml up -d
docker compose --env-file deploy/hetzner/.env \
  -f deploy/hetzner/docker-compose.yml ps
```

Add both routes from `Caddyfile.shopauth.snippet` to ShopAuth's Caddyfile,
validate it, and reload Caddy. `X-Forwarded-Proto` must be `https`, otherwise
Django's production SSL redirect loops behind Cloudflare Flexible.

## Codex MCP

After the web app has a user and an Instagram account is connected:

```bash
codex mcp add brightbean --url https://studio.shopauth.cloud/api/v1/mcp
codex mcp login brightbean
```

Codex supports Streamable HTTP servers with OAuth. BrightBean also supports a
scoped `bb_studio_...` bearer API key when OAuth is not desirable.

## Instagram Direct

Create a Meta app that uses Instagram Login and register this exact redirect:

```text
https://studio.shopauth.cloud/social-accounts/callback/instagram_login/
```

The Instagram account must be Professional (Business or Creator). Required
permissions include content publishing; comment/message permissions are used by
the inbox automation surfaces.
