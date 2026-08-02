# Pre-submission evidence checklist

## Deployment and public identity

- [ ] Current branch reviewed and deployed to production.
- [ ] Migration `0013_youtube_authorization_retention` applied successfully.
- [ ] Background worker running and both recurring tasks registered: `schedule_all_health_checks` and `purge_invalid_youtube_authorizations`.
- [ ] `https://studio.shopauth.cloud/youtube-integration/` returns HTTP 200 without login and describes the app.
- [ ] Privacy, Terms and Data Deletion URLs return HTTP 200 without login and show “Effective and last updated: August 2, 2026”.
- [ ] Public pages use the same product name and logo as the OAuth consent screen.
- [ ] `shopauth.cloud` ownership verified in Google Search Console by a Google Cloud project owner/editor.

## Google Cloud configuration

- [ ] Correct project selected: `micro-reef-504311-n9`.
- [ ] YouTube Data API v3 and YouTube Analytics API enabled.
- [ ] OAuth app user type External and publishing status Production.
- [ ] Home page, Privacy Policy and Terms URLs exactly match this package.
- [ ] Authorized domain includes `shopauth.cloud`.
- [ ] Web-client redirect URI exactly matches `https://studio.shopauth.cloud/social-accounts/callback/youtube/` including scheme and trailing slash.
- [ ] Scope list exactly matches the scopes requested by the production app.
- [ ] User support and developer-contact emails are monitored.
- [ ] No client ID/secret mismatch between Google Cloud and production secret configuration.

## Product behavior

- [ ] Connect flow shows Google OAuth under the BrightBean Social Studio name.
- [ ] Connected channel identity matches YouTube Studio.
- [ ] Composer requires/shows title, description, made-for-kids and visibility controls.
- [ ] Public, Unlisted and Private options are visible before submit.
- [ ] A private test Short uploads and reaches processed/succeeded state.
- [ ] No automatic `#Shorts` or other undisclosed text is appended to the user title/description.
- [ ] YouTube analytics are labeled and shown only to authorized workspace users.
- [ ] Comment UI is live if `youtube.force-ssl` is requested.
- [ ] In-product Disconnect is easy to find.
- [ ] Disconnect on a test connection revokes/removes the grant and deletes the local account data.

## Evidence files

- [ ] Screenshot: public product page with URL.
- [ ] Screenshot: Privacy Policy Google/YouTube section and Limited Use statement.
- [ ] Screenshot: Data Deletion page and Google security-settings link.
- [ ] Screenshot: OAuth consent app name, domain and full scope list.
- [ ] Screenshot: connected channel card beside matching YouTube Studio channel.
- [ ] Screenshot: composer YouTube panel with visibility selector.
- [ ] Screenshot: completed private upload in BrightBean and YouTube Studio.
- [ ] Screenshot: YouTube-labeled analytics.
- [ ] Screenshot: YouTube comment/reply surface.
- [ ] Unlisted reviewer demo URL accessible in an incognito window.
- [ ] Combined dossier PDF and scope-justification PDF each under 10 MB.

## Final consistency check

- [ ] App name, URLs, project ID, scopes, use-case copy and demo all agree.
- [ ] Every described feature is available to the reviewer account.
- [ ] Every requested scope is visibly demonstrated.
- [ ] Owner/legal identity and expected user/channel counts are filled with real values.
- [ ] Demo credentials are supplied only through Google's secure form, never in Git or PDFs.
- [ ] Submit OAuth verification and YouTube API compliance audit separately, then monitor the project-owner inbox and spam folder for reviewer questions.
