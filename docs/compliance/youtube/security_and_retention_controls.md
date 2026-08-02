# Security and retention controls

## Implemented controls

- OAuth access and refresh tokens are stored in encrypted database fields.
- OAuth `state` is signed, tied to the workspace/user/platform, and time-limited.
- The Google OAuth callback URI is HTTPS and fixed to the production domain.
- Social-account management requires authentication and the `manage_social_accounts` permission.
- YouTube actions are scoped to a selected workspace and connected account.
- Composer validation restricts YouTube visibility to `public`, `unlisted`, or `private` and title length to YouTube's 100-character limit.
- The service requests no Google password and does not log token values.
- Connected-account authorization is normally verified every six hours.
- Confirmed YouTube authorization failures start a 30-day recovery/deletion clock; successful reauthorization clears the clock.
- A daily task deletes connected YouTube API data after 30 days of continuously invalid authorization.
- In-product disconnect revokes the OAuth grant and immediately deletes the connected account and related API-derived data.
- Organization hard deletion attempts token revocation before cascade deletion removes credentials.
- The full raw YouTube upload response is no longer retained; a migration scrubs response payloads from existing YouTube publishing rows while preserving user-selected publishing settings.
- Analytics records and publishing records cascade-delete with the connected social account.

## Operational controls required at deployment

- Run migrations before enabling the new code path.
- Run the background-task worker continuously so the six-hour authorization checks and daily retention purge execute.
- Restrict production environment and database access to authorized operators.
- Keep the Google OAuth client secret only in the production secret store/environment; never in the repository or audit attachments.
- Keep Google Cloud project owner/editor contacts current and monitor review mail.
- Review failed health-check and retention-purge logs without recording token values.
- Re-run the evidence checklist after any change to scopes, redirect URI, domain, app name, logo, privacy URL, or YouTube feature set.

## Deletion behavior

Disconnecting in BrightBean affects BrightBean-held authorization and data. It does not delete videos or other content held independently by YouTube. The public Data Deletion page explains that users must use YouTube controls to delete YouTube-hosted content.
