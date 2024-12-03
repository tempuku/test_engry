from django.contrib.auth.models import User


class CustomUser(User):
    @property
    def is_active(self) -> bool:
        return self.is_active
