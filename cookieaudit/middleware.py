import hashlib
import random
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.db.utils import DatabaseError, ProgrammingError, OperationalError
from .models import CookieEvent

def _client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

class CookieAuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not getattr(settings, "COOKIEAUDIT_ENABLED", True):
            return None

        allowlist = set(getattr(settings, "COOKIEAUDIT_ALLOWLIST", []))
        if not allowlist:
            return None

        sample_rate = float(getattr(settings, "COOKIEAUDIT_SAMPLE_RATE", 1.0))
        if sample_rate < 1.0 and random.random() > sample_rate:
            return None

        user = getattr(request, "user", None)
        user = user if (user and user.is_authenticated) else None

        for name, value in request.COOKIES.items():
            if name not in allowlist:
                continue
            s = str(value)
            preview = s[:120]
            value_hash = hashlib.sha256(s.encode("utf-8")).hexdigest()

            try:
                CookieEvent.objects.create(
                    path=request.path[:512],
                    method=request.method[:10],
                    user=user,
                    session_key=getattr(request.session, "session_key", "") or "",
                    client_ip=_client_ip(request),
                    user_agent=request.META.get("HTTP_USER_AGENT", "")[:1024],
                    cookie_name=name[:128],
                    cookie_value_preview=preview,
                    value_sha256=value_hash,
                )
            except (DatabaseError, ProgrammingError, OperationalError):
                # Table may not exist yet on first deploy; skip logging
                pass

        return None
