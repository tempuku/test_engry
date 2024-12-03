import secrets

from django.contrib.auth import get_user_model
from django.db import models


class TgToken(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        related_name="tokens",
        verbose_name="User",
    )
    value = models.CharField(max_length=32, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = self.generate_unique_token()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_token():
        return secrets.token_hex(32)

    class Meta:
        db_table = "tg_token"
