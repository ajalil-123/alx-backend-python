
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        # Add custom logic if needed
        return user
