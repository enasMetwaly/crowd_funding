from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import date
from django.utils.http import base36_to_int
from django.utils.crypto import constant_time_compare, salted_hmac

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_token_with_timestamp(self, user, timestamp):
        """
        Generate a token by combining the user's primary key and a timestamp.
        """
        # Combine the user's primary key and timestamp
        token = f"{user.id}-{timestamp}"
        return token

    def make_token(self, user):
        """
        Generate a token for the given user.
        """
        timestamp = self._num_days(self._today())
        # Call the _make_token_with_timestamp method with user and timestamp
        return self._make_token_with_timestamp(user, timestamp)

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return False

        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False

        # Check the timestamp is within limit
        if (self._num_days(self._today()) - ts) > 1:
            return False

        return True

    def _num_days(self, dt):
        return (dt - date(2001, 1, 1)).days

    def _today(self):
        # Used for mocking in tests
        return date.today()
