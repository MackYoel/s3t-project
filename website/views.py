from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import PersonForm
from django.urls import reverse
from django.http import HttpResponse
from website.functions import send_email, create_unique_token
from accounts.functions import generate_username
from s3t.settings import DOMAIN_NAME
from django.contrib.auth.decorators import login_required
from website.forms import ProductForm
from accounts.models import Person
from website.models import Product


@login_required()
def panel(request):
    return render(request, 'website/panel.html')


def providers(request):
    providers = Person.objects.filter(is_superuser=False)
    return render(request, 'website/providers/list.html', locals())


def new_provider(request):
    if request.method == 'POST' and request.POST:
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.username = person.email
            token = create_unique_token()
            msg = 'Por favor haga <a href="{}{}">click aqui</a> para asignar una contraseña a su cuenta.'
            msg = msg.format(DOMAIN_NAME, reverse('set_password_provider', kwargs={'token': token}))
            err = send_email(subject='S3T - Asigne contrasenia',
                             from_email='junior.yc9@gmail.com',
                             to_email=person.email,
                             content=msg)
            if not err:
                person.token = token
                person.save()
                return redirect(reverse('providers'))
            return HttpResponse("""
                <script>
                    alert("ha ocurrido un error enviando el correo al proveedor");
                    window.location.href = '%s';
                </script>""" % reverse('providers'))
    else:
        title = 'Nuevo Proveedor'
        form = PersonForm()

    comeback_to = 'providers'
    return render(request, 'hook/form.html', locals())


def products(request):
    from toctochi_stereo import pprint
    pprint(request.GET, label='request.GET')

    if request.method == 'GET':
        if not request.GET or not request.GET.get('provider'):
            products = Product.objects.all()
        else:
            try:
                provider_pk = int(request.GET.get('provider'))
            except:
                products = Product.objects.all()
            else:
                if provider_pk:
                    products = Product.objects.filter(provider=provider_pk)

    providers = Person.objects.filter(is_superuser=False)
    is_admin = request.user.is_superuser
    if not is_admin:
        title = 'Mis Productos'
    else:
        title = 'Tienda de Productos'

    # if is_provider:
    return render(request, 'website/products/provider_list.html', locals())
    # else:


def edit_provider(request, pk):
    provider = get_object_or_404(Person, pk=int(pk))
    title = 'Editar Proveedor'
    comeback_to = 'providers'

    if request.method == 'POST' and request.POST:
        form = PersonForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect(reverse('providers'))
        else:
            return render(request, 'hook/form.html', locals())

    form = PersonForm(instance=provider)
    return render(request, 'hook/form.html', locals())


def set_password_provider(request, token):
    provider = get_object_or_404(Person, token=token)
    return render(request, 'website/providers/set_password.html', locals())


def new_product(request):
    comeback_to = 'products'
    # import pdb
    # from toctochi_stereo import pprint
    if request.method == 'POST' and request.POST:
        # pdb.set_trace()
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.provider = request.user.person
            product.save()
            return redirect(reverse('products'))
        else:
            return render(request, 'hook/form.html', locals())

    title = 'Nuevo Producto'
    form = ProductForm()
    return render(request, 'hook/form.html', locals())


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=int(pk))
    title = 'Editar Producto'
    comeback_to = 'products'

    if request.method == 'POST' and request.POST:
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('products'))
        else:
            return render(request, 'hook/form.html', locals())

    form = ProductForm(instance=product)
    return render(request, 'hook/form.html', locals())
