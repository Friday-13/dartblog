from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's primary key, user active status and 
        that's sure to change after account activation to produce a token that is
        invalidated when it's used:
        1. The is_active field will change upon an account activation.
        Failing those things, settings.PASSWORD_RESET_TIMEOUT eventually
        invalidates the token.

        Running this data through salted_hmac() prevents password cracking
        attempts using the reset token, provided the secret isn't compromised.
        """
        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
        return f"{user.pk}{timestamp}{user.is_active}"

account_activation_token = AccountActivationTokenGenerator()
