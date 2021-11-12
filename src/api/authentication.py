from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _


def get_system_user():
    username_system = "System"
    first_name = "System"
    user_system = User.objects.filter(username=username_system).first()
    if user_system:
        return user_system
    else:
        return User.objects.create_user(
            username_system, None, None, first_name=first_name, is_staff=True, is_active=False, is_superuser=True
        )


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Clients should authenticate by passing the API Key in the "API-Key"
    HTTP header.  For example:

        API-Key: bc5c7613-543d-432e-a03d-aacb1a2afa61
    """

    def authenticate(self, request):
        api_key = request.META.get('HTTP_API_KEY', '')
        if not api_key:
            return None

        elif len(api_key.split()) > 2:
            msg = _('Invalid API-Key header. Value should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        if api_key == 'bc5c7613-543d-432e-a03d-aacb1a2afa61':
            user = get_system_user()
            return (user, None)
        else:
            msg = _('Invalid API-Key.')
            raise exceptions.AuthenticationFailed(msg)
