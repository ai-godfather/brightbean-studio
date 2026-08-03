# YouTube Data API Services Audit and Quota Extension Form

Field-by-field draft for the current form at
`https://support.google.com/youtube/contact/yt_api_form?hl=en`.

Prepared: 2026-08-03

Submission status: **DRAFT — DO NOT SUBMIT YET**. Values marked
Remaining values marked `OWNER INPUT REQUIRED` must be supplied by the account
owner. Reviewer credentials and the owner's telephone number must be entered only in Google's secure form and
must never be committed to the repository.

## Verified production and Google Cloud facts

- Google Cloud project name: `BrightBean Studio YouTube`
- Google Cloud project ID: `micro-reef-504311-n9`
- Google Cloud project number: `648393702117`
- API Client name: `BrightBean Social Studio`
- Google account currently opening the form: `mediainteractiveai@gmail.com`
- Production application: `https://studio.shopauth.cloud/`
- Public YouTube product page: `https://studio.shopauth.cloud/youtube-integration/`
- Privacy Policy: `https://studio.shopauth.cloud/privacy/`
- Terms of Service: `https://studio.shopauth.cloud/terms/`
- Data Deletion Instructions: `https://studio.shopauth.cloud/data-deletion/`
- Login URL: `https://studio.shopauth.cloud/accounts/login/`
- OAuth redirect URI: `https://studio.shopauth.cloud/social-accounts/callback/youtube/`
- Current OAuth publishing status: `Testing` (must be changed to `Production` before submission)
- Owner channel: `https://www.youtube.com/@godfather.a.i`
- Domain ownership: owner-reported Search Console DNS verification completed on 2026-08-03

The previous pre-deployment check returned HTTP 200 for all five URLs on
2026-08-02. After deploying this revision, repeat the check and require the
four public product/legal pages to show the revision date August 3, 2026 before
submitting the form.

## Section 1: Request Type

### Select the reason for your request

Select:

> Complete a compliance audit to request for additional quota

This is the only first-audit path in the current form. In Section 5 select
**No change / Default quota**. We are not asking for a quota increase; the
purpose is the compliance audit required to lift the private-only restriction
for uploads from the production API project.

Do not select the re-audit option unless Google has explicitly requested a
periodic re-audit for this project.

## Section 2: Organization and Contact Information

### Application type

- If ShopAuth Cloud is a registered business/entity, select: **As an
  organization or on behalf of an organization or registered entity**.
- If no registered entity operates the service, select: **As an individual
  user** and use the responsible person's legal details.

### Legal and address fields

| Form field | Answer |
|---|---|
| Your Full Legal Name | `Piotr Kwiatkowski` |
| Your Organization's Legal Name | `Not applicable — individual applicant. ShopAuth Cloud is a service/brand name, not a registered legal entity.` |
| Parent Company Name | Leave blank unless legally applicable |
| Organization's Primary Website | `https://studio.shopauth.cloud/youtube-integration/` |
| Country | `Other (please specify)` |
| Country — other | `Poland` |
| Street Address | `ul. Ludowa 9A` |
| City | `Michałowice` |
| State/Province | `Mazowieckie` |
| Postal Code | `05-816` |
| Category | `Creator Tools and Services` |
| Business type | `Independent Developer/Sole Proprietor` — use this combined form option while applying as an individual content creator, not as a registered organization |

### Contacts

Recommended if the project-owner mailbox is monitored:

| Form field | Answer |
|---|---|
| Primary contact name | `Piotr Kwiatkowski` |
| Primary contact email | `mediainteractiveai@gmail.com` |
| Primary technical contact | Select `Same as Primary Contact` |
| Primary business contact | Select `Same as Primary Contact` |

The public support and privacy contact remains `admin@shopauth.cloud`.

## Section 3: Business Model and Google Contacts

### Describe your organization's work as it relates to YouTube

Paste:

> BrightBean Social Studio is a web-based social-media content-planning,
> approval, scheduling, publishing, comment-management and analytics workspace
> for channel owners and authorized teams. A user explicitly connects their
> YouTube channel through Google OAuth and confirms the authenticated channel
> identity. The user selects a video or Short, reviews the title, description,
> tags, made-for-kids declaration and Public, Unlisted or Private visibility,
> then initiates or schedules the upload. BrightBean uses the resumable
> videos.insert flow and stores the returned video ID as the publication
> result. Authorized users can view comment threads, post a first comment,
> reply to comments, and view YouTube-labeled channel/video analytics. YouTube
> API data is available only to the channel owner or authorized workspace
> members. BrightBean does not scrape or download YouTube media, sell YouTube
> API data, profile viewers, manipulate engagement, or train generalized AI
> models on YouTube API data.

### Primary audience

Select only:

- `Individual Content Creators (YouTubers, influencers)`

### Monetization

Select:

- `Recurring Subscriptions (users pay monthly/yearly)`
- `Freemium (free version with paid upgrades)`

Rationale: the Studio has a free/pre-activation surface and offers paid
per-organization Intelligence subscriptions. YouTube API data and YouTube
access are not sold separately and are not used for advertising.

### Advertising follow-up

- Select `Not applicable` for selling advertisements or sponsorships on or
  within YouTube content/the YouTube player.
- The written-commercial-use-approval follow-up should not appear. If it does,
  do not claim approval that has not been received.

### Google relationship and identifiers

| Form field | Answer |
|---|---|
| Google/YouTube representative | `No, I do not have a Google representative` unless the owner has a current named representative |
| How did you first learn about the YouTube Data API? | `Google Developer Documentation` — owner must confirm this subjective answer before submission |
| Content Owner ID(s) | Leave blank; BrightBean is not using YouTube Content Manager on behalf of a content owner |
| Associated Channel URL | Leave blank because no Content Owner ID is supplied |
| Google Ads Customer ID(s) | Leave blank; BrightBean is not using its own Ads Customer ID to manage campaigns for others in this integration |

## Section 4: API Client Overview and Access Information

| Form field | Answer |
|---|---|
| API Client Name | `BrightBean Social Studio` |
| Does the name contain "YouTube"? | `No` |
| Primary Access URL | `https://studio.shopauth.cloud/` |
| Privacy Policy URL | `https://studio.shopauth.cloud/privacy/` |
| Terms of Service URL | `https://studio.shopauth.cloud/terms/` |
| Is the API Client publicly accessible? | `Yes` |
| Demo Account Username or Email | `[OWNER INPUT REQUIRED: dedicated reviewer account]` |
| Demo Account Password | `[ENTER ONLY IN GOOGLE'S SECURE FORM; NEVER COMMIT]` |
| Login URL | `https://studio.shopauth.cloud/accounts/login/` |

### Special Instructions for Access

Paste after replacing the bracketed workspace/channel values:

> Sign in with the provided dedicated reviewer credentials and open the
> [REVIEWER WORKSPACE] workspace. Open Social Accounts and select the dedicated
> reviewer-owned YouTube channel [TEST CHANNEL NAME/URL]. To review OAuth,
> choose Connect and approve the four displayed YouTube permissions. Open New
> / Publish, choose the preloaded harmless test MP4, select the YouTube target,
> enter a title and description, show Tags and Made for Kids, choose Private,
> and submit. The resulting YouTube video ID is shown in BrightBean and the
> matching private upload can be viewed in YouTube Studio. Analytics is under
> Analytics; comments are under Social Inbox with the YouTube filter. Use only
> the dedicated reviewer connection. Disconnect it only after completing the
> review.

Select the demo-account acknowledgment only after the owner has reviewed and
accepted its wording.

## Section 5: Use Cases and Quota Extension Details

### Project and use cases

| Form field | Answer |
|---|---|
| How many project numbers are you adding? | `1` |
| Google Cloud Project Number | `648393702117` |
| Use cases | `Video Uploading & Account Management`; `Tools for Creators`; `Analytics & Reporting` |
| Does the API Client require Google OAuth 2.0 sign-in? | `Yes` |
| Analytics derived-metrics/data-storage acknowledgment | Select only after reviewing the linked policy |
| Expected API Usage Volume | `Fewer than 1,000 requests per day` |

### Endpoints actually used by the production code

Select exactly:

- `youtube.channels.list`
- `youtube.videos.insert`
- `youtube.thumbnails.set`
- `youtube.commentThreads.insert`
- `youtube.commentThreads.list`
- `youtube.comments.insert`
- `youtube.videos.list`

Do not select `youtube.comments.setModerationStatus`: the production provider
does not call that endpoint. Do not select `youtube.comments.list`: replies are
read through `commentThreads.list` with the `replies` part. Do not select
`youtube.videos.update`: metadata and visibility are supplied during
`videos.insert`.

The YouTube Analytics API `reports.query` calls are covered by the Analytics &
Reporting use case and the analytics acknowledgment; that endpoint is not one
of the Data API endpoint checkboxes in this form.

### Quota

- What total quota are you requesting? Select
  `No change / Default quota (10k quota points)`.
- Do not select the separate additional-quota checkbox for
  `youtube.search.list`.
- Do not select the separate additional-quota checkbox for
  `youtube.videos.insert`.

Current default allocation is 100 `videos.insert` calls/day in its separate
upload bucket, 100 `search.list` calls/day in its separate search bucket, and
10,000 units/day for the remaining endpoints. BrightBean additionally limits
publishing to 6 YouTube uploads per connected account per day unless an
explicit administrative override exists.

If the form unexpectedly requires a quota justification despite selecting no
change, paste:

> No quota extension is requested. This submission seeks the compliance audit
> required to lift the private-only upload restriction on the production
> project. BrightBean expects fewer than 1,000 API requests per day during the
> initial rollout and enforces a product limit of six YouTube uploads per
> connected account per day unless an explicit administrative override is
> configured.

### Required evidence fields for Project #1

Each field accepts one JPEG, PNG or PDF file.

| Form upload field | File to provide | Status |
|---|---|---|
| Privacy Policy Screenshots | `pdf/BrightBean_Privacy_Policy_2026-08-03.pdf` | Ready after regeneration; live URL also required |
| Homepage Screenshot | `projects/brightbean-youtube-oauth-review-demo/snapshots/sc01_public_identity.png` | Ready; shows YouTube branding and Privacy/Terms/Data deletion links |
| Terms of Service Documentation | `pdf/BrightBean_Terms_of_Service_2026-08-03.pdf` | Ready after regeneration; live URL also required |
| Conditional Evidence | `[CREATE FINAL COMBINED PDF: OAuth consent + upload interface + genuine live analytics + genuine live comment thread/reply]` | Blocked; do not use the reconstructed analytics/comments image as primary evidence |

## Section 6: Additional Evidence and Documentation

These fields are optional but recommended:

| Form upload field | Recommended file |
|---|---|
| Architecture Diagram | `[CREATE FINAL ARCHITECTURE DIAGRAM after exact deployed components are confirmed]` |
| User Flow Diagrams | `projects/brightbean-youtube-oauth-review-demo/assets/images/sc02-connect-start-guide.png` — label it as a guide, not a recording of the Connect click |
| Other Supporting Materials | `pdf/BrightBean_YouTube_API_Audit_Dossier.pdf` |

If only one supporting file is allowed, use the audit dossier rather than the
separate scope-justification PDF because the dossier is the broader record.

## Section 7: Attestations and Submission

The owner must personally review and, if true, select all required items:

- YouTube API Services Terms of Service
- Google Privacy Policy
- responsibility for current and future Developer Policy compliance
- termination understanding
- demo-account terms waiver, if a demo account is provided
- accuracy and completeness of the submission
- consent to processing the submission data
- support recording consent

Do not pre-check these boxes on the owner's behalf. Do not submit the form
without an explicit final instruction after all blockers below are closed.

## Submission blockers

1. Supply the telephone number requested by the form only in Google's secure
   form, confirm how the owner first learned about the API, and approve a
   realistic 3/6/12-month channel forecast.
2. Create a dedicated BrightBean reviewer account and a low-risk reviewer-owned
   YouTube test channel; provide the password only in the form.
3. Upload a square BrightBean Social Studio app logo, change OAuth publishing
   status from `Testing` to `Production`, and capture a fresh OAuth screenshot/video.
4. Capture genuine live Analytics UI. The existing reconstructed image is
   clearly labeled as a reconstruction and is not acceptable as primary
   reviewer evidence.
5. Create an owner-controlled test comment, capture the live YouTube-filtered
   thread and a harmless reply in BrightBean, and confirm it in YouTube Studio.
   The form and scope copy must not claim moderation because the production
   provider does not call a moderation endpoint.
6. Build the final single conditional-evidence PDF from the corrected OAuth,
   upload, analytics, comments and revocation evidence.
7. Review every Section 7 attestation and the analytics data-storage
   acknowledgment immediately before submission.
