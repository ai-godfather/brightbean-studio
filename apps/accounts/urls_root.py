from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path(
        "privacy/",
        TemplateView.as_view(template_name="legal/privacy_policy.html"),
        name="privacy_policy",
    ),
    path(
        "terms/",
        TemplateView.as_view(template_name="legal/terms_of_service.html"),
        name="terms_of_service",
    ),
    path(
        "data-deletion/",
        TemplateView.as_view(template_name="legal/data_deletion.html"),
        name="data_deletion",
    ),
    path(
        "youtube-integration/",
        TemplateView.as_view(template_name="legal/youtube_integration.html"),
        name="youtube_integration",
    ),
    path("", views.dashboard, name="dashboard"),
]
