from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CookieEvent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    path = models.CharField(max_length=512)
    method = models.CharField(max_length=10)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, blank=True)
    client_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    cookie_name = models.CharField(max_length=128, db_index=True)
    # Store a short preview and a hash to avoid keeping full sensitive values
    cookie_value_preview = models.CharField(max_length=128, blank=True)
    value_sha256 = models.CharField(max_length=64, blank=True)

    class Meta:
        managed = True
        db_table = 'tracking_cookie_cookieevent'
        

    def __str__(self):
        return f"{self.cookie_name} @ {self.created_at:%Y-%m-%d %H:%M:%S}"
