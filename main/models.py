from django.contrib.auth.models import User
from django.db import models
from accounts.models import Person

from django.utils.translation import ugettext as _


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    provider = models.ForeignKey(Person)
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='images')
    size = models.CharField(max_length=50)
    price = models.FloatField()
    available = models.BooleanField(default=True, blank=True)
    colors = models.ManyToManyField(Color, null=True, blank=True)

    @property
    def get_colors(self):
        return ', '.join([c.name for c in self.colors.all()])

    def __str__(self):
        return self.name


class Order(models.Model):
    PENDING = 0
    SENT = 1
    RECEIVED = 2
    CHECKED = 3
    PAID = 4

    ORDER_STATES = (
        (PENDING, 'Pendiente de atención'),
        (SENT, 'Enviado por el proveedor'),
        (RECEIVED, 'Recibido por el cliente'),
        (CHECKED, 'Revisado por el cliente'),
        (PAID, 'Pagado al proveedor')
    )

    provider = models.ForeignKey(Person, related_name='order_provider')
    sub_total = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    paid = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    state = models.IntegerField(default=PENDING, choices=ORDER_STATES)

    code = models.CharField(max_length=20, null=True, blank=True)
    transport_name = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    note_received = models.TextField(null=True, blank=True)

    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    received_at = models.DateTimeField(_("received at"), null=True, blank=True)
    checked_at = models.DateTimeField(_("checked at"), null=True, blank=True)
    paid_at = models.DateTimeField(_("paid at"), null=True, blank=True)

    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return self.provider.get_full_name()


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    observation = models.TextField()
    total = models.FloatField(default=0)
    note = models.CharField(max_length=250, blank=True, null=True)


class Payment(models.Model):
    order = models.ForeignKey(Order)
    amount = models.FloatField()
    observation = models.CharField(max_length=200, null=True, blank=True)

    voucher_image = models.ImageField(upload_to='vouchers', null=True, blank=True)
    voucher_code = models.CharField(max_length=20, null=True, blank=True)

    paid_at = models.DateTimeField(_("paid at"), null=True, blank=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)


class CarSession(models.Model):
    user = models.ForeignKey(User)
    provider = models.ForeignKey(Person, related_name='provider')
    observation = models.TextField()
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    note = models.CharField(max_length=250)
