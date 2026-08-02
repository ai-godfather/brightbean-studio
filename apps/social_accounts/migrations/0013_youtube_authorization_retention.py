from django.db import migrations, models


YOUTUBE_USER_CONTROLLED_KEYS = {
    "category_id",
    "post_type",
    "privacy_status",
    "self_declared_made_for_kids",
    "tags",
    "thumbnail_asset_id",
}


def scrub_stored_youtube_upload_responses(apps, schema_editor):
    PlatformPost = apps.get_model("composer", "PlatformPost")
    rows = PlatformPost.objects.filter(social_account__platform="youtube").exclude(platform_extra={})
    for row in rows.iterator():
        current = row.platform_extra or {}
        sanitized = {key: current[key] for key in YOUTUBE_USER_CONTROLLED_KEYS if key in current}
        if sanitized != current:
            row.platform_extra = sanitized
            row.save(update_fields=["platform_extra"])


class Migration(migrations.Migration):
    dependencies = [
        ("composer", "0015_per_account_status"),
        ("social_accounts", "0012_add_devto_platform"),
    ]

    operations = [
        migrations.AddField(
            model_name="socialaccount",
            name="authorization_invalid_since",
            field=models.DateTimeField(
                blank=True,
                help_text="First confirmed OAuth authorization failure; used for API-data retention enforcement.",
                null=True,
            ),
        ),
        migrations.RunPython(scrub_stored_youtube_upload_responses, migrations.RunPython.noop),
    ]
