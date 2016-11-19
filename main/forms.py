from django.forms import ModelForm, CheckboxSelectMultiple, DateInput
from .models import Product, Color, Order
from .functions import add_form_control_class, update_form_labels, add_form_required


class MyDateInput(DateInput):
    input_type = 'date'


class OrderPaymentForm(ModelForm):
    class Meta:
        model = Order
        fields = ('amount_paid', 'paid_done_at', 'voucher_code', 'voucher_image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            'amount_paid': 'Monto pagado *',
            'paid_done_at': 'Fecha de pago *',
            'voucher_code': 'Número de operación',
            'voucher_image': 'Imagen del recibo',
        }
        update_form_labels(self, labels)
        self.fields['amount_paid'].widget.attrs.update({'required': 'true'})
        self.fields['paid_done_at'].widget = MyDateInput()
        self.fields['paid_done_at'].widget.attrs.update({'required': 'true'})
        add_form_control_class(self.fields)

        # self.fields['note'].widget.attrs.update({'placeholder': 'ejm. descripcion del empaquetamiento'})


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
