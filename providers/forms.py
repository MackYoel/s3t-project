from django.forms import ModelForm, CheckboxSelectMultiple

from main.models import Order
from main.models import Product, Color
from main.functions import add_form_control_class, update_form_labels, add_form_required


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'size', 'price', 'available', 'colors')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        labels = {
            'name': 'Nombre *',
            'size': 'Talla *',
            'image': 'Imagen',
            'price': 'Precio *',
            'available': 'Habilitado'
        }
        update_form_labels(self, labels)

        self.fields["colors"].widget = CheckboxSelectMultiple()
        self.fields["colors"].queryset = Color.objects.all()


class OrderProviderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('code', 'transport_name', 'note')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_form_control_class(self.fields)
        labels = {
            'code': 'Numero de guia *',
            'transport_name': 'Empresa de Transporte *',
            'note': 'Detalle de Empaque *',
        }
        update_form_labels(self, labels)
        add_form_required(self.fields)

        self.fields['note'].widget.attrs.update({'placeholder': 'ejm. descripcion del empaquetamiento'})
