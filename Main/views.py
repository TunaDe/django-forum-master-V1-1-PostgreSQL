from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render


def privacy_policy_page(request):
    """
    Render the responsive HTML Privacy Policy page.
    Uses template: Main/templates/legal/privacy_policy.html
    """
    return render(
        request,
        "legal/privacy_policy.html",
        {"last_updated": "09.01.2026"},
    )


def privacy_policy_download(request):
    """Download the project's Privacy Policy PDF.

    Note: The PDF currently lives in Main/templates.
    """
    pdf_path = Path(settings.BASE_DIR) / "Main" / "templates" / "Privacy_Policy.pdf"

    try:
        return FileResponse(
            pdf_path.open("rb"),
            as_attachment=True,
            filename="Privacy_Policy.pdf",
            content_type="application/pdf",
        )
    except FileNotFoundError as exc:
        raise Http404("Privacy policy file not found") from exc
