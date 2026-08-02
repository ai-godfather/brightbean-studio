# Reviewer demo script and shot list

Target length: 4–6 minutes. Capture a real desktop browser at 1440×900 or 1920×1080. Keep the address bar visible when showing public URLs and the OAuth domain. Zoom the browser so scope text and selected values are legible. Use a dedicated reviewer account and test YouTube channel.

## Narration and shots

### 00:00–00:25 — Product identity and public pages

Show `https://studio.shopauth.cloud/youtube-integration/` with the address bar visible.

Narration: “This is BrightBean Social Studio, operated by ShopAuth Cloud. The YouTube integration lets an authorized channel owner plan and upload videos or Shorts, manage comments, and view channel analytics. The product page links to the public Privacy Policy, Terms of Service, and Data Deletion Instructions.”

Open each legal link briefly. On Privacy, show the Google/YouTube section, Limited Use statement, Google Privacy Policy link, Google security-settings link, retention, and deletion language.

### 00:25–01:15 — Login and OAuth initiation

Sign in to the dedicated reviewer account. Open the reviewer workspace → Social Accounts → Add/Connect → YouTube.

Narration: “Only a signed-in workspace member with social-account management permission can initiate this connection. BrightBean never asks for the user's Google password.”

Show the Google OAuth page. Keep the product name and domain legible. Expand details so every requested scope is visible. Narrate each scope using the short explanations from `scope_justifications.md`. Complete consent with the reviewer-owned Google account.

### 01:15–01:40 — Connected channel identity

Return to BrightBean and show the connected channel card. In another tab, show the same channel in YouTube Studio.

Narration: “BrightBean reads the authenticated channel identity so the user can confirm the correct publishing target. This channel name and handle match the reviewer-owned channel in YouTube Studio.”

### 01:40–03:00 — User-controlled upload

Open New/Publish. Select the YouTube test account and a harmless short MP4. Show:

- YouTube channel target
- title field and 100-character behavior
- description
- tags
- made-for-kids selection
- custom thumbnail control, if used
- visibility selector with Public, Unlisted and Private

Select **Private** for the review upload.

Narration: “The user reviews the media and YouTube metadata and explicitly selects visibility before upload. BrightBean supports public, unlisted and private. For this reviewer demonstration I am choosing Private. BrightBean does not append undisclosed text or change visibility after the user submits.”

Submit/publish. Show publishing progress and completion with the YouTube video ID or link. Open YouTube Studio and show the matching private upload.

### 03:00–04:05 — Read, comments and analytics scopes

Open the YouTube-labeled Analytics view for the connected channel. Show the date selector and available YouTube metrics. Do not present cross-platform aggregate or derived scores as YouTube metrics.

Narration: “The read-only and analytics scopes identify the selected channel and provide owner-authorized YouTube channel and video metrics, including views, watch time and average view percentage. This information is shown only to the channel owner or authorized workspace members and is labeled as YouTube data.”

Open the YouTube comments or Social Inbox view. Show a test comment thread and, if the deployed UI supports it, post a harmless reply on the reviewer-owned test content.

Narration: “The force-ssl scope supports the implemented comment-reading, reply and moderation features. BrightBean does not use it to like, subscribe, or manipulate engagement.”

### 04:05–04:45 — Revocation and deletion controls

Return to Social Accounts and point to Disconnect without clicking it on a production connection. Open the Data Deletion page and the Google third-party connections link.

Narration: “The user can disconnect the channel here. BrightBean then attempts immediate programmatic token revocation and deletes the connected YouTube API data. The user can also revoke access from Google settings. If authorization becomes invalid outside BrightBean, the service stops new access and deletes associated YouTube API data within 30 days.”

### 04:45–05:00 — Close

Return to the public product page.

Narration: “Support and privacy requests are handled at admin@shopauth.cloud. The public policies and product description are available without signing in.”

## Recording safety

- Use a dedicated reviewer Google account and test YouTube channel.
- Blur or avoid email inboxes, unrelated browser tabs, tokens, client secrets, recovery codes, server consoles, and production customer data.
- Never open the Google Cloud Credentials secret screen in the recording.
- Use Private for the test upload; the audit is about app behavior, not public distribution of the demo asset.
- If the current production channel must be disconnected to re-record OAuth, obtain explicit owner approval first.
