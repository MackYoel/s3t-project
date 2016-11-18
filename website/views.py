from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from accounts.forms import PersonForm
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from website.functions import send_email, create_unique_token, json
from accounts.functions import generate_username
from s3t.settings import DOMAIN_NAME, FROM_EMAIL
from django.contrib.auth.decorators import login_required
from website.forms import ProductForm
from accounts.models import Person
from website.models import Product, CarSession


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
            msg = msg.format(DOMAIN_NAME, reverse('accounts:set_password', kwargs={'token': token}))
            err = send_email(subject='S3T - Asigne contrasenia',
                             from_email=FROM_EMAIL,
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


@login_required()
def products(request):
    if request.user.is_staff:
        return redirect('car')
    products = Product.objects.filter(provider=request.user)
    title = 'Mis Productos'
    return render(request, 'website/products/list.html', locals())


@login_required()
@staff_member_required
def car(request):
    provider_pk = request.GET.get('provider', None)
    if provider_pk:
        provider = get_object_or_404(Person, pk=provider_pk)
        products = Product.objects.filter(provider=provider_pk)
    else:
        provider_pk = 0
        products = Product.objects.all()
    title = 'Tienda de Productos'
    providers = Person.objects.filter(is_staff=False)
    products_in_car = CarSession.objects.filter(user=request.user)
    return render(request, 'website/car/product_list.html', locals())


@login_required()
@staff_member_required
@csrf_exempt
def car_add_product(request):
    result = {}
    if request.method == 'POST':
        product_pk = request.POST['product_pk']
        product = get_object_or_404(Product, pk=product_pk)
        if product:
            try:
                CarSession.objects.get(user=request.user, product=product)
                result["success"] = False
                result["message"] = _('The product is already added')
            except CarSession.DoesNotExist:
                CarSession.objects.create(user=request.user, product=product)
                result["success"] = True
    else:
        result["success"] = False
        result["message"] = _('Bad Request')
    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required()
@staff_member_required
@csrf_exempt
def car_remove_product(request):
    result = {}
    if request.method == 'POST':
        product_pk = request.POST['product_pk']
        product = get_object_or_404(Product, pk=product_pk)
        if product:
            try:
                car_session = CarSession.objects.get(user=request.user, product=product)
                car_session.delete()
                result["success"] = True
            except CarSession.DoesNotExist:
                result["success"] = False
                result["message"] = _('The product is not in the car')
    else:
        result["success"] = False
        result["message"] = _('Bad Request')
    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required()
@staff_member_required
def car_update_quantity(request):
    title = 'Tienda de Productos, actualización de cantidades'
    products_in_car = CarSession.objects.filter(user=request.user)
    products = list()
    for p in products_in_car:
        products.append(p.product)
    return render(request, 'website/car/update_quantity.html', locals())


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

            for color in form.cleaned_data['colors']:
                product.colors.add(color)

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
