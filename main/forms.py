from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Product, Color, Order
from .functions import add_form_control_class, update_form_labels, add_form_required


class OrderClientForm(ModelForm):
    class Meta:
        model = Order
        fields = ( 'voucher_code', 'voucher_image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        labels = {
            'voucher_code': 'Número de operación *',
            'voucher_image': 'Imagen del recibo',
        }
        update_form_labels(self, labels)
        self.fields['voucher_code'].widget.attrs.update({'required': 'true'})

        # self.fields['note'].widget.attrs.update({'placeholder': 'ejm. descripcion del empaquetamiento'})
