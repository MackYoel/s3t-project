from django.forms import ModelForm
from website.models import Product
from website.functions import add_form_control_class, update_form_labels


class ProductForm(ModelForm):
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

    class Meta:
        model = Product
        fields = ('name', 'image',
                  'size', 'price', 'available')
