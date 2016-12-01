from django.forms import ModelForm, CheckboxSelectMultiple, DateInput
from .models import Product, Color, Order, Payment
from .functions import add_form_control_class, update_form_labels, add_form_required


class MyDateInput(DateInput):
    input_type = 'date'


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'paid_at', 'observation', 'voucher_code', 'voucher_image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            'amount': 'Monto por pagar *',
            'paid_at': 'Fecha de pago *',
            'observation': 'Nota',
            'voucher_code': 'Número de operación',
            'voucher_image': 'Imagen del recibo',
        }
        update_form_labels(self, labels)
        self.fields['amount'].widget.attrs.update({'required': 'true'})

        initial_extra = kwargs.pop('initial', None)
        if initial_extra:
            amount = initial_extra['amount']
            self.fields['amount'].widget.attrs.update({'max': amount, 'min': 1})
        else:
            amount = 0

        self.fields['amount'].widget.attrs.update({'placeholder': 'total deuda: '+ str(amount)})

        self.fields['paid_at'].widget = MyDateInput()
        self.fields['paid_at'].widget.attrs.update({'required': 'true'})

        add_form_control_class(self.fields)


class OrderReceivedForm(ModelForm):
    class Meta:
        model = Order
        fields = ('note_received',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        labels = {
            'note_received': 'Nota de revisado *',
        }
        update_form_labels(self, labels)
        self.fields['note_received'].widget.attrs.update({'required': 'true'})
