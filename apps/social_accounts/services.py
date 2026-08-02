"""Lifecycle helpers for connected social accounts."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def revoke_social_account_token(account) -> bool:
    """Best-effort revocation without logging or returning any token value.

    Google accepts either an access token or a refresh token at its revocation
    endpoint. Prefer the refresh token for YouTube so the long-lived grant is
    invalidated; other providers keep the established access-token behavior.
    """
    from apps.publisher.engine import _resolve_publish_credentials
    from providers import get_provider

    token = account.oauth_access_token
    if account.platform == "youtube" and account.oauth_refresh_token:
        token = account.oauth_refresh_token
    if not token:
        return True

    try:
        provider = get_provider(account.platform, _resolve_publish_credentials(account))
        revoked = bool(provider.revoke_token(token))
        if not revoked:
            logger.warning("Provider did not confirm token revocation for social account %s", account.pk)
        return revoked
    except Exception:
        logger.exception("Failed to revoke token for social account %s", account.pk)
        return False
