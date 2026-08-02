# Google OAuth verification submission

## App configuration

| Field | Value |
|---|---|
| Google Cloud project ID | `micro-reef-504311-n9` |
| App name | `BrightBean Social Studio` |
| User type | External |
| Publishing status | Production before submission |
| App home page | `https://studio.shopauth.cloud/youtube-integration/` |
| Privacy Policy | `https://studio.shopauth.cloud/privacy/` |
| Terms of Service | `https://studio.shopauth.cloud/terms/` |
| Authorized domain | `shopauth.cloud` |
| User support email | `admin@shopauth.cloud` |
| Developer contact email | `admin@shopauth.cloud` plus an actively monitored project-owner address |
| OAuth client type | Web application |
| Authorized redirect URI | `https://studio.shopauth.cloud/social-accounts/callback/youtube/` |

The OAuth consent screen, public product page, app UI, and demo narration must all use the same product name: **BrightBean Social Studio**. If the Google Cloud console currently shows `shopauth.cloud`, update it before recording the final demo.

## App purpose

BrightBean Social Studio is a web-based content-planning and publishing workspace for channel owners and authorized social-media teams. A user connects a YouTube channel through Google OAuth, selects a target channel, prepares a video or Short with a title, description, tags, made-for-kids setting, and explicit public/unlisted/private visibility, and then initiates or schedules the upload. Authorized users can also manage YouTube comments and review channel and video analytics inside their workspace.

The integration does not download YouTube media, scrape YouTube, sell Google user data, create surveillance profiles, manipulate engagement, or publish without a user-selected target and publication settings.

## Paste-ready scope summary

BrightBean Social Studio requests four YouTube scopes to provide implemented, user-facing features: upload of user-selected videos and Shorts; identification and display of the user's selected channel; comment viewing, posting, replying and moderation; and owner-authorized channel/video analytics. Each action is initiated by an authorized workspace user. Tokens are encrypted, authorization is checked regularly, raw upload API responses are not retained, and disconnecting the channel revokes the grant and deletes stored YouTube API data. Detailed per-scope explanations are in `scope_justifications.md`.

## Demo video requirements

The final unlisted reviewer video must show, in one continuous and legible recording:

1. The public application home page and legal links.
2. Sign-in to the BrightBean reviewer account.
3. Social Accounts → YouTube → Connect.
4. The Google OAuth screen showing the same app name and every requested scope.
5. Selection of the reviewer-owned YouTube channel.
6. Composer setup for a Short, including title, description, tags, made-for-kids setting, and visibility selector.
7. A private test upload initiated by the reviewer account.
8. The completed BrightBean status and matching private video in YouTube Studio.
9. The analytics and comments surfaces that justify the read, force-ssl, and analytics scopes.
10. The in-product Disconnect control and the Data Deletion page. Do not actually disconnect the production channel in the final take unless a dedicated test connection is used.

## Owner inputs required before submission

- `[OWNER INPUT REQUIRED]` Confirm the legal entity/person responsible for ShopAuth Cloud and ensure the same identity is used where Google asks for organization details.
- `[OWNER INPUT REQUIRED]` Confirm an actively monitored Google Cloud project-owner/editor email.
- `[OWNER INPUT REQUIRED]` Verify domain ownership for `shopauth.cloud` in Google Search Console using a project owner or editor.
- `[OWNER INPUT REQUIRED]` Confirm the app logo and brand name match the public page and OAuth consent screen.
- `[OWNER INPUT REQUIRED]` Create a dedicated reviewer account and test YouTube channel; provide credentials only in the secure submission form.
