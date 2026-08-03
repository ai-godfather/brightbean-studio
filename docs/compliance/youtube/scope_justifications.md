# OAuth scope justifications

## `https://www.googleapis.com/auth/youtube.upload`

BrightBean Social Studio uses this scope to upload a video or Short selected by the signed-in user to the YouTube channel that the user connected. Before upload, the composer lets the user review and set the title, description, tags, made-for-kids declaration, and public/unlisted/private visibility. The user explicitly initiates immediate publication or chooses a schedule. A narrower read-only scope cannot upload the user's media.

Demo evidence: connect the reviewer channel, open the composer, select a test MP4, show all YouTube settings, choose **Private**, initiate the upload, and show the matching private video in YouTube Studio.

## `https://www.googleapis.com/auth/youtube.readonly`

BrightBean Social Studio uses this scope to retrieve the authenticated user's own channel identity and current channel metadata so the user can verify the correct publishing target. The product displays the channel name, handle, avatar and owner-authorized channel statistics, and uses the YouTube video ID to retrieve current status and metrics for videos published through the workspace. The upload-only scope does not provide the read access needed to identify the selected channel or display current channel/video state.

Demo evidence: after OAuth, show the connected channel card with the same channel name and handle as YouTube Studio, then show a YouTube-specific analytics view with source labels.

## `https://www.googleapis.com/auth/youtube.force-ssl`

BrightBean Social Studio uses this scope for implemented comment-management features on the authorized user's channel: reading comment threads, posting a first comment when requested, and replying to comments from the Social Inbox. These write actions require an authorized YouTube scope; `youtube.readonly` cannot create comments or replies. BrightBean does not use this scope to subscribe, like, manipulate engagement, or call a comment-moderation endpoint.

Demo evidence: open the YouTube comments/inbox surface, show a comment thread, post a harmless test reply on the reviewer-owned private/unlisted test content, and show the corresponding result in YouTube Studio. If the deployed UI does not expose these actions at submission time, remove this scope from both code/consent configuration or finish the UI before submitting.

## `https://www.googleapis.com/auth/yt-analytics.readonly`

BrightBean Social Studio uses this read-only scope to display owner-authorized YouTube channel and video analytics such as views, estimated minutes watched, average view percentage, subscriber changes and shares. Analytics are shown only to the channel owner or authorized workspace members and are clearly labeled as YouTube data. The YouTube Data API read scope does not provide YouTube Analytics reports such as watch time or average view percentage.

Demo evidence: open Analytics, select the connected YouTube channel, show the YouTube-labeled metrics and date range, and explain that the scope is read-only. If YouTube analytics is disabled in production at submission time, remove this scope from the OAuth consent screen and do not include it in the request.

## Minimum-scope decision

All four scopes correspond to currently implemented product functions. No scope is requested for future features. BrightBean does not request broad Google account, Gmail, Drive, Photos, viewing-history, subscription-management, or monetization scopes.
