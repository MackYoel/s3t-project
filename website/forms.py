from django.forms import ModelForm, CheckboxSelectMultiple
from website.models import Product, Color
from website.functions import add_form_control_class, update_form_labels


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
