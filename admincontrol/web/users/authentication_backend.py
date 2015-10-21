from web.users.models import AeeUser


class EmailAuthenticationBackend(object):
    # noinspection PyMethodMayBeStatic
    def authenticate(self, username=None, password=None):

        try:
            user = AeeUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except AeeUser.DoesNotExist:
            return None

    # noinspection PyMethodMayBeStatic
    def get_user(self, user_id):
        try:
            user = AeeUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except AeeUser.DoesNotExist:
            return None
