# YouTube API Services audit — paste-ready answers

## Request type

Select the option for an **API compliance audit** required for an unverified API project / public upload access. Do not request additional quota unless the product actually needs more than the existing quota.

## Applicant and organization

- Applicant name: `[OWNER INPUT REQUIRED: full legal name]`
- Organization/legal entity: `[OWNER INPUT REQUIRED: exact registered name or state that this is an individual/sole trader]`
- Address: `[OWNER INPUT REQUIRED]`
- Phone: `[OWNER INPUT REQUIRED]`
- Contact email: `admin@shopauth.cloud` plus the actively monitored Google Cloud project owner address
- Website: `https://studio.shopauth.cloud/youtube-integration/`

## API project and client

- Google Cloud project ID: `micro-reef-504311-n9`
- Google Cloud project number: `[OWNER INPUT REQUIRED: copy from Google Cloud Project info; do not infer from the client ID]`
- API client name: `BrightBean Social Studio`
- API client type: server-side web application
- Production URL: `https://studio.shopauth.cloud/`
- Public product page: `https://studio.shopauth.cloud/youtube-integration/`
- Privacy Policy: `https://studio.shopauth.cloud/privacy/`
- Terms of Service: `https://studio.shopauth.cloud/terms/`
- Data Deletion: `https://studio.shopauth.cloud/data-deletion/`
- OAuth redirect URI: `https://studio.shopauth.cloud/social-accounts/callback/youtube/`

## Detailed use case

BrightBean Social Studio is a web-based social-media content-planning, approval, scheduling, publishing, comment-management and analytics workspace. A channel owner or authorized team member signs in to BrightBean, opens Social Accounts, and explicitly connects a YouTube channel through Google's OAuth consent flow. BrightBean retrieves the authenticated channel identity so the user can confirm the target.

For publishing, the user selects a video file, chooses the connected YouTube channel, reviews or enters the video title and description, optionally sets tags and a custom thumbnail, declares whether the content is made for kids, and explicitly selects Public, Unlisted or Private visibility. The user then initiates immediate publication or sets a schedule. BrightBean uses the resumable `videos.insert` upload flow and stores the returned YouTube video ID as the publication result. BrightBean does not retain the full raw upload response.

When the user enables comments and analytics, BrightBean lets the authorized channel team view and reply to YouTube comments and view YouTube-labeled channel/video analytics. YouTube API data is visible only to the channel owner or authorized members of that workspace. The client does not scrape, download YouTube media, sell API data, profile viewers, manipulate engagement, or create derived YouTube scores.

## How users initiate YouTube actions

Every OAuth connection is initiated by a user with workspace permission to manage social accounts. Every upload has a selected YouTube target and a visible composer panel for title, description, tags, made-for-kids status and privacy. Public, unlisted and private are separate choices. Immediate upload or scheduled upload follows a user submit action. Comment replies and moderation are initiated from the YouTube-labeled inbox. BrightBean does not change an existing video's visibility without explicit user selection.

## Data storage and retention

OAuth tokens are encrypted. Channel identity/profile data is refreshed during authorization health checks, normally every six hours. YouTube analytics/statistics may be retained as dated historical data while the channel remains authorized and the metrics are needed to provide the owner-requested analytics feature; authorization is reconfirmed at least every 30 days. Other YouTube Authorized Data is refreshed or deleted within 30 days. Raw upload API responses are not retained.

In-product disconnect attempts immediate programmatic token revocation and deletes the connected-account record and related API-derived publishing/analytics data. If BrightBean detects that YouTube authorization can no longer be verified, it stops new access, retries health checks during a recovery window, and automatically deletes the connected YouTube API data after no more than 30 days. Users can also request deletion by email or revoke access from Google's third-party connections settings.

## Expected API usage

- Product-level safety limit: maximum 6 YouTube publishes per connected account per day unless an explicit per-account administrative override is configured.
- Standard project quota assumption: 10,000 quota units/day.
- One resumable `videos.insert` flow per user-approved upload.
- Channel profile/authorization health check: normally every 6 hours per active account.
- Account analytics: normally daily.
- Video analytics: hourly for posts under 24 hours, every 6 hours for posts aged 1–7 days, daily for posts aged 7–30 days, weekly for posts aged 30–90 days, then background refresh stops.
- Initial rollout: a small number of owner-managed channels. `[OWNER INPUT REQUIRED: provide realistic expected connected-channel count for 3, 6 and 12 months.]`

## Quota request

No additional quota is requested in this submission unless the owner selects otherwise. The goal is the compliance audit needed to permit user-selected public/unlisted uploads from the production project. If the form requires a numeric request, use the current default quota and explain that no extension is requested.

## User control and deletion

Users can disconnect a channel from Social Accounts. BrightBean immediately removes the connection and stored YouTube API data and attempts to revoke the OAuth grant. The Privacy Policy links to Google's third-party connections settings. BrightBean explains that deleting BrightBean-held data does not delete content held independently on YouTube.

## Demo access

- Reviewer login URL: `https://studio.shopauth.cloud/accounts/login/`
- Reviewer email: `[OWNER INPUT REQUIRED: dedicated reviewer account]`
- Reviewer password: `[PROVIDE ONLY IN THE FORM'S SECURE FIELD; NEVER COMMIT]`
- Reviewer YouTube channel: `[OWNER INPUT REQUIRED: dedicated test channel name and URL]`
- Instructions: sign in, open Social Accounts, connect/select the reviewer-owned YouTube channel, then open Publish/New to view the YouTube composer settings. A preloaded harmless test MP4 should be available. Use Private visibility for the review upload unless the reviewer requests otherwise.

## Attached evidence

Attach the combined audit dossier PDF and, if the form permits, the scope-justification PDF. Provide the unlisted demo-video URL in the video field. Legal policies should be submitted as live public URLs; PDFs are supporting snapshots, not replacements for public pages.
