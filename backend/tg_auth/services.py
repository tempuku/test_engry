from typing import Optional

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import TgToken


class TgTokenService:
    """
    Service to encapsulate all business logic related to tokens.
    """

    @staticmethod
    def validate_token(auth_key: str) -> Optional[TgToken]:
        """
        Validates the provided token.

        :param auth_key: The token value to validate.
        :return: A valid TgToken object if it exists, otherwise None.
        """
        try:
            token = TgToken.objects.get(value=auth_key)
            return token
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_from_token(token: TgToken) -> Optional[User]:
        """
        Retrieves the user associated with the token.

        :param token: TgToken object
        :return: User object if it exists and is active, otherwise None.
        """
        if user := token.user:
            if user.is_active:
                return user
        return None

    @staticmethod
    def get_new_token() -> TgToken:
        return TgToken.objects.create()
