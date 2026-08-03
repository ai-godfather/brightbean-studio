"""Inbox reply delivery contracts."""

from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.inbox.models import InboxMessage, InboxReply
from apps.members.models import OrgMembership, WorkspaceMembership
from apps.organizations.models import Organization
from apps.social_accounts.models import SocialAccount
from apps.workspaces.models import Workspace
from providers.types import OAuthTokens, ReplyResult


class InboxReplyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reply-owner@example.com",
            password="testpass123",
            tos_accepted_at=timezone.now(),
        )
        self.organization = Organization.objects.create(name="Reply Test Org")
        self.workspace = Workspace.objects.create(
            organization=self.organization,
            name="Reply Test Workspace",
        )
        OrgMembership.objects.create(
            user=self.user,
            organization=self.organization,
            org_role=OrgMembership.OrgRole.OWNER,
        )
        WorkspaceMembership.objects.create(
            user=self.user,
            workspace=self.workspace,
            workspace_role=WorkspaceMembership.WorkspaceRole.OWNER,
        )
        self.account = SocialAccount.objects.create(
            workspace=self.workspace,
            platform="youtube",
            account_platform_id="youtube-channel-1",
            account_name="YouTube Test Channel",
            oauth_access_token="expired-access-token",
            oauth_refresh_token="refresh-token",
            token_expires_at=timezone.now() - timedelta(minutes=5),
            connection_status=SocialAccount.ConnectionStatus.CONNECTED,
        )
        self.message = InboxMessage.objects.create(
            workspace=self.workspace,
            social_account=self.account,
            platform_message_id="youtube-comment-1",
            message_type=InboxMessage.MessageType.COMMENT,
            sender_name="Reviewer",
            body="Test comment",
            received_at=timezone.now(),
        )
        self.client.force_login(self.user)
        self.url = reverse(
            "inbox:send_reply",
            kwargs={"workspace_id": self.workspace.id, "message_id": self.message.id},
        )

    @patch("apps.inbox.views.get_provider")
    @patch("apps.publisher.engine._resolve_publish_credentials", return_value={})
    def test_refreshes_expiring_token_before_posting_reply(self, _resolve_credentials, get_provider):
        provider = get_provider.return_value
        provider.refresh_token.return_value = OAuthTokens(
            access_token="fresh-access-token",
            refresh_token="refresh-token",
            expires_in=3600,
        )
        provider.reply_to_message.return_value = ReplyResult(platform_message_id="youtube-reply-1")

        response = self.client.post(self.url, {"body": "OAuth reviewer reply"})

        self.assertEqual(response.status_code, 200)
        provider.refresh_token.assert_called_once_with("refresh-token")
        provider.reply_to_message.assert_called_once_with(
            access_token="fresh-access-token",
            message_id="youtube-comment-1",
            text="OAuth reviewer reply",
            extra={},
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.oauth_access_token, "fresh-access-token")
        self.assertTrue(
            InboxReply.objects.filter(
                inbox_message=self.message,
                platform_reply_id="youtube-reply-1",
            ).exists()
        )
