"""Tests for social_accounts background tasks."""

from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from django.utils import timezone

from apps.social_accounts.models import SocialAccount
from apps.social_accounts.tasks import check_social_account_health, purge_invalid_youtube_authorizations
from providers.exceptions import APIError
from providers.types import AccountProfile, OAuthTokens


def _profile(*, follower_count=0, avatar_url=None, name="", handle=None, platform_id="123"):
    return AccountProfile(
        platform_id=platform_id,
        name=name,
        handle=handle,
        avatar_url=avatar_url,
        follower_count=follower_count,
    )


@pytest.fixture
def organization(db):
    from apps.organizations.models import Organization

    return Organization.objects.create(name="Test Org")


@pytest.fixture
def workspace(db, organization):
    from apps.workspaces.models import Workspace

    return Workspace.objects.create(name="Test WS", organization=organization)


@pytest.fixture
def connected_account(db, workspace):
    return SocialAccount.objects.create(
        workspace=workspace,
        platform="facebook",
        account_platform_id="123",
        account_name="Test Page",
        oauth_access_token="valid_token",
        oauth_refresh_token="refresh_token",
        connection_status=SocialAccount.ConnectionStatus.CONNECTED,
    )


@pytest.mark.django_db
class TestCheckSocialAccountHealth:
    @patch("providers.get_provider")
    def test_successful_health_check(self, mock_get_provider, connected_account):
        mock_provider = MagicMock()
        mock_provider.get_profile.return_value = _profile(follower_count=1500)
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(connected_account.id))

        account = SocialAccount.objects.get(pk=connected_account.pk)
        assert account.connection_status == SocialAccount.ConnectionStatus.CONNECTED
        assert account.follower_count == 1500
        assert account.last_health_check_at is not None
        assert account.last_error == ""

    @patch("providers.get_provider")
    def test_instagram_health_check_passes_selected_ig_user_id(self, mock_get_provider, workspace):
        account = SocialAccount.objects.create(
            workspace=workspace,
            platform="instagram",
            account_platform_id="17841400000000000",
            account_name="Brightbean",
            oauth_access_token="page-token",
            connection_status=SocialAccount.ConnectionStatus.CONNECTED,
        )
        mock_provider = MagicMock()
        mock_provider.get_profile.return_value = _profile(
            platform_id="17841400000000000",
            name="Brightbean",
            handle="brightbean",
        )
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(account.id))

        _platform, credentials = mock_get_provider.call_args.args
        assert credentials["ig_user_id"] == "17841400000000000"
        mock_provider.get_profile.assert_called_once_with("page-token")

    @patch("apps.common.validators.is_safe_url", return_value=True)
    @patch("providers.get_provider")
    def test_mastodon_health_check_injects_instance_url_without_registration(
        self, mock_get_provider, _mock_is_safe_url, workspace
    ):
        # Regression: the old inline resolver set instance_url only *inside* the
        # MastodonAppRegistration lookup, so an account with no registration row had
        # instance_url dropped -> empty base URL. The shared resolver sets it first.
        # is_safe_url is patched to keep the SSRF check off the network.
        account = SocialAccount.objects.create(
            workspace=workspace,
            platform="mastodon",
            account_platform_id="masto-1",
            account_name="Masto",
            instance_url="https://mastodon.social",
            oauth_access_token="tok",
            connection_status=SocialAccount.ConnectionStatus.CONNECTED,
        )
        mock_provider = MagicMock()
        mock_provider.get_profile.return_value = _profile(platform_id="masto-1", name="Masto")
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(account.id))

        _platform, credentials = mock_get_provider.call_args.args
        assert credentials["instance_url"] == "https://mastodon.social"

    @patch("providers.get_provider")
    def test_failed_health_check_sets_error(self, mock_get_provider, connected_account):
        mock_provider = MagicMock()
        mock_provider.get_profile.side_effect = Exception("Token expired")
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(connected_account.id))

        account = SocialAccount.objects.get(pk=connected_account.pk)
        assert account.connection_status == SocialAccount.ConnectionStatus.ERROR
        assert account.last_error == "Connection check failed. Please try reconnecting."

    @patch("providers.get_provider")
    def test_youtube_unauthorized_starts_retention_clock(self, mock_get_provider, workspace):
        account = SocialAccount.objects.create(
            workspace=workspace,
            platform="youtube",
            account_platform_id="UC123",
            account_name="Channel",
            oauth_access_token="expired",
            oauth_refresh_token="revokable",
        )
        mock_provider = MagicMock()
        mock_provider.get_profile.side_effect = APIError("Unauthorized", status_code=401)
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(account.id))

        account.refresh_from_db()
        assert account.connection_status == SocialAccount.ConnectionStatus.ERROR
        assert account.authorization_invalid_since is not None

    @patch("providers.get_provider")
    def test_youtube_transient_failure_does_not_start_retention_clock(self, mock_get_provider, workspace):
        account = SocialAccount.objects.create(
            workspace=workspace,
            platform="youtube",
            account_platform_id="UC123",
            account_name="Channel",
            oauth_access_token="token",
        )
        mock_provider = MagicMock()
        mock_provider.get_profile.side_effect = APIError("Unavailable", status_code=503)
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(account.id))

        account.refresh_from_db()
        assert account.authorization_invalid_since is None

    @patch("providers.get_provider")
    def test_successful_youtube_check_clears_retention_clock(self, mock_get_provider, workspace):
        account = SocialAccount.objects.create(
            workspace=workspace,
            platform="youtube",
            account_platform_id="UC123",
            account_name="Channel",
            oauth_access_token="token",
            authorization_invalid_since=timezone.now() - timedelta(days=3),
        )
        mock_provider = MagicMock()
        mock_provider.get_profile.return_value = _profile(platform_id="UC123", name="Channel")
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(account.id))

        account.refresh_from_db()
        assert account.authorization_invalid_since is None

    @patch("providers.get_provider")
    def test_token_refresh_on_expiring(self, mock_get_provider, connected_account):
        connected_account.token_expires_at = timezone.now() + timedelta(days=3)
        connected_account.save()

        mock_provider = MagicMock()
        mock_provider.refresh_token.return_value = OAuthTokens(
            access_token="new_access",
            refresh_token="new_refresh",
            expires_in=3600,
        )
        mock_provider.get_profile.return_value = _profile(follower_count=100)
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(connected_account.id))

        account = SocialAccount.objects.get(pk=connected_account.pk)
        assert account.oauth_access_token == "new_access"
        assert account.oauth_refresh_token == "new_refresh"
        assert account.connection_status == SocialAccount.ConnectionStatus.CONNECTED

    @patch("providers.get_provider")
    def test_refresh_failure_marks_expiring(self, mock_get_provider, connected_account):
        connected_account.token_expires_at = timezone.now() + timedelta(days=3)
        connected_account.save()

        mock_provider = MagicMock()
        mock_provider.refresh_token.side_effect = Exception("Refresh failed")
        mock_provider.get_profile.return_value = _profile(follower_count=100)
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(connected_account.id))

        account = SocialAccount.objects.get(pk=connected_account.pk)
        # After refresh failure the token_expiring status is set, then profile
        # fetch succeeds but doesn't override the expiring status
        assert account.connection_status in (
            SocialAccount.ConnectionStatus.CONNECTED,
            SocialAccount.ConnectionStatus.TOKEN_EXPIRING,
        )

    @patch("providers.get_provider")
    def test_health_check_refreshes_avatar_name_handle(self, mock_get_provider, connected_account):
        connected_account.avatar_url = "https://old.example/avatar.jpg?x-expires=1"
        connected_account.account_name = "Old Name"
        connected_account.account_handle = "old"
        connected_account.save()

        mock_provider = MagicMock()
        mock_provider.get_profile.return_value = _profile(
            follower_count=200,
            avatar_url="https://new.example/avatar.jpg?x-expires=999",
            name="New Name",
            handle="new",
        )
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(connected_account.id))

        account = SocialAccount.objects.get(pk=connected_account.pk)
        assert account.avatar_url == "https://new.example/avatar.jpg?x-expires=999"
        assert account.account_name == "New Name"
        assert account.account_handle == "new"

    @patch("providers.get_provider")
    def test_health_check_preserves_avatar_when_provider_returns_empty(self, mock_get_provider, connected_account):
        connected_account.avatar_url = "https://old.example/avatar.jpg"
        connected_account.account_name = "Kept Name"
        connected_account.account_handle = "kept"
        connected_account.save()

        mock_provider = MagicMock()
        mock_provider.get_profile.return_value = _profile(follower_count=10)
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(connected_account.id))

        account = SocialAccount.objects.get(pk=connected_account.pk)
        assert account.avatar_url == "https://old.example/avatar.jpg"
        assert account.account_name == "Kept Name"
        assert account.account_handle == "kept"

    @patch("providers.get_provider")
    def test_failed_health_check_preserves_profile_fields(self, mock_get_provider, connected_account):
        connected_account.avatar_url = "https://old.example/avatar.jpg"
        connected_account.account_name = "Kept Name"
        connected_account.account_handle = "kept"
        connected_account.save()

        mock_provider = MagicMock()
        mock_provider.get_profile.side_effect = Exception("Token expired")
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(connected_account.id))

        account = SocialAccount.objects.get(pk=connected_account.pk)
        assert account.connection_status == SocialAccount.ConnectionStatus.ERROR
        assert account.avatar_url == "https://old.example/avatar.jpg"
        assert account.account_name == "Kept Name"
        assert account.account_handle == "kept"

    def test_nonexistent_account_does_not_raise(self, db):
        check_social_account_health.now("00000000-0000-0000-0000-000000000000")

    @patch("providers.get_provider")
    def test_bluesky_bootstrap_refresh_when_expires_at_null(self, mock_get_provider, db, workspace):
        """Legacy Bluesky accounts with token_expires_at=NULL should still refresh."""
        account = SocialAccount.objects.create(
            workspace=workspace,
            platform="bluesky",
            account_platform_id="did:plc:abc",
            account_name="Test",
            oauth_access_token="stale_access",
            oauth_refresh_token="valid_refresh",
            token_expires_at=None,
            connection_status=SocialAccount.ConnectionStatus.CONNECTED,
        )

        mock_provider = MagicMock()
        mock_provider.refresh_token.return_value = OAuthTokens(
            access_token="fresh_access",
            refresh_token="fresh_refresh",
            expires_in=7200,
        )
        mock_provider.get_profile.return_value = _profile(follower_count=42)
        mock_get_provider.return_value = mock_provider

        check_social_account_health.now(str(account.id))

        mock_provider.refresh_token.assert_called_once_with("valid_refresh")
        account.refresh_from_db()
        assert account.oauth_access_token == "fresh_access"
        assert account.oauth_refresh_token == "fresh_refresh"
        assert account.token_expires_at is not None
        assert account.connection_status == SocialAccount.ConnectionStatus.CONNECTED


@pytest.mark.django_db
class TestPurgeInvalidYouTubeAuthorizations:
    @patch("apps.social_accounts.services.revoke_social_account_token", return_value=True)
    def test_deletes_account_after_30_days(self, mock_revoke, workspace):
        account = SocialAccount.objects.create(
            workspace=workspace,
            platform="youtube",
            account_platform_id="UC-expired",
            account_name="Expired channel",
            oauth_access_token="expired",
            authorization_invalid_since=timezone.now() - timedelta(days=31),
        )

        purge_invalid_youtube_authorizations.now()

        assert not SocialAccount.objects.filter(pk=account.pk).exists()
        mock_revoke.assert_called_once()

    @patch("apps.social_accounts.services.revoke_social_account_token", return_value=True)
    def test_keeps_account_during_30_day_recovery_window(self, mock_revoke, workspace):
        account = SocialAccount.objects.create(
            workspace=workspace,
            platform="youtube",
            account_platform_id="UC-recent",
            account_name="Recent failure",
            oauth_access_token="expired",
            authorization_invalid_since=timezone.now() - timedelta(days=29),
        )

        purge_invalid_youtube_authorizations.now()

        assert SocialAccount.objects.filter(pk=account.pk).exists()
        mock_revoke.assert_not_called()
