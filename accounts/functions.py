from django.contrib.auth.models import User

__author__ = 'bicho'


def generate_username(base, correlative=''):
    if ' ' in base:
        base = base[:base.index(' ')]
    username = base + str(correlative)
    try:
        User.objects.get(username=username)
        if correlative == '':
            correlative = 0
        correlative = int(correlative)
        correlative += 1
        return generate_username(username, str(correlative))
    except User.DoesNotExist:
        return username
