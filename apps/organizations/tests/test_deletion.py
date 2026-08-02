from unittest.mock import patch

import pytest

from apps.organizations.models import Organization
from apps.social_accounts.models import SocialAccount
from apps.workspaces.models import Workspace


@pytest.mark.django_db
def test_hard_delete_revokes_social_tokens_before_cascade():
    organization = Organization.objects.create(name="Delete Me")
    workspace = Workspace.objects.create(name="Workspace", organization=organization)
    account = SocialAccount.objects.create(
        workspace=workspace,
        platform="youtube",
        account_platform_id="UC123",
        account_name="Channel",
        oauth_access_token="access",
        oauth_refresh_token="refresh",
    )

    with patch("apps.social_accounts.services.revoke_social_account_token", return_value=True) as mock_revoke:
        organization.hard_delete()

    mock_revoke.assert_called_once()
    assert mock_revoke.call_args.args[0].pk == account.pk
    assert not Organization.objects.filter(pk=organization.pk).exists()
