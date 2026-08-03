# BrightBean YouTube verification package

Prepared: 2026-08-03

This directory is the source package for two separate Google reviews:

1. Google OAuth app verification for the sensitive YouTube scopes.
2. YouTube API Services compliance audit to remove the private-only upload restriction applied to unverified API projects.

The reviews are related but not interchangeable. Complete OAuth verification in Google Auth Platform and submit the YouTube audit form as separate requests.

## Submission assets

- `oauth_verification_submission.md` — exact Google Auth Platform settings and copy.
- `youtube_api_audit_responses.md` — paste-ready answers for the YouTube audit form.
- `scope_justifications.md` — one justification per requested OAuth scope.
- `data_handling_matrix.md` — accessed data, use, storage, refresh, sharing, and deletion.
- `security_and_retention_controls.md` — implemented safeguards and retention controls.
- `reviewer_demo_script.md` — narrated, time-coded recording plan.
- `evidence_checklist.md` — screenshots and checks required before submission.
- `SUBMISSION_RUNBOOK_PL.md` — Polish owner runbook and remaining human inputs.
- `pdf/` — generated upload-ready PDFs.

## Rebuild the PDFs

From the repository root:

```bash
uv run --no-project --with-requirements docs/compliance/youtube/requirements.txt \
  python docs/compliance/youtube/build_audit_pdfs.py
```

## Public URLs after deployment

- Application home page: https://studio.shopauth.cloud/youtube-integration/
- Privacy Policy: https://studio.shopauth.cloud/privacy/
- Terms of Service: https://studio.shopauth.cloud/terms/
- Data Deletion Instructions: https://studio.shopauth.cloud/data-deletion/
- OAuth redirect URI: https://studio.shopauth.cloud/social-accounts/callback/youtube/

Do not submit until the current branch has been reviewed, deployed, migrated, and all four public pages return HTTP 200 with the 2026-08-03 revision.

## Sensitive material

Never commit OAuth client secrets, access tokens, refresh tokens, user passwords, recovery codes, or reviewer demo passwords. If a form requests demo-account credentials, create a dedicated low-risk reviewer account and provide the credentials only through the form's secure field.
