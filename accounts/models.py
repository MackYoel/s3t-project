from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class Person(User):
    MAN = 0
    WOMAN = 1

    SEX = (
        (MAN, _('man')),
        (WOMAN, _('woman')),
    )

    # TODO dni turn it to unique
    # TODO dni show in patient
    dni = models.IntegerField(null=True, blank=True)
    sex = models.IntegerField(_("sex"), choices=SEX, default=MAN)

    def __str__(self):
        return self.get_full_name() + ' | ' + self.email

    # TODO clean_dni