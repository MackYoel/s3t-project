# coding=utf-8

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from accounts.models import Person
from .forms import ProductForm, OrderProviderForm
from main.models import Product, Order, OrderItem, Payment


@login_required()
def panel(request):
    return render(request, 'main/panel.html')


@login_required()
def product_list(request):
    if request.user.is_staff:
        provider_pk = int(request.GET.get('provider', 0))
        if provider_pk > 0:
            provider = get_object_or_404(Person, pk=provider_pk)
            products = Product.objects.filter(provider=provider)
        else:
            products = Product.objects.all()
        title = 'Productos de ' + provider.get_full_name()
    else:
        products = Product.objects.filter(provider=request.user)
        title = 'Mis Productos'
    return render(request, 'providers/products/list.html', locals())


@login_required()
def product_new(request):
    comeback_to = 'providers:product_list'
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

            return redirect(reverse('providers:product_list'))
        else:
            return render(request, 'hook/form_layout.html', locals())

    title = 'Nuevo Producto'
    form = ProductForm()
    return render(request, 'hook/form_layout.html', locals())


@login_required()
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=int(pk))
    title = 'Editar Producto'
    comeback_to = 'providers:product_list'

    if request.method == 'POST' and request.POST:
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('providers:product_list'))
        else:
            return render(request, 'hook/form_layout.html', locals())

    form = ProductForm(instance=product)
    return render(request, 'hook/form_layout.html', locals())


@login_required()
def order_list(request):
    orders = Order.objects.filter(provider=request.user).order_by('-created_at')
    return render(request, 'providers/orders/list.html', locals())


@login_required()
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk, provider=request.user)
    title = 'Pedido'
    comeback_to = 'providers:order_list'
    order_items = OrderItem.objects.filter(order=order)

    if order.state == order.PENDING or order.state == order.ACCEPTED:
        save_text = 'Enviar a Junior'
        form_title = 'Transporte'
        if request.POST:
            acept_reject = request.POST.get('acept_reject', None)
            if acept_reject:
                order.state = acept_reject
                order.accepted_at = datetime.now()
                order.save()
                return redirect(reverse('providers:order_edit', args=(order.pk,)))
            else:
                form = OrderProviderForm(request.POST, instance=order)
                if form.is_valid():
                    order = form.save(commit=False)
                    order.sent_at = datetime.now()
                    order.state = Order.SENT
                    order.save()
        else:
            form = OrderProviderForm(instance=order)

    payments = Payment.objects.filter(order=order)
    total_paid = Payment.objects.filter(order=order).aggregate(total_amount=Sum('amount'))
    if total_paid:
        total_paid = total_paid['total_amount']
        try:
            total_paid = float(total_paid)
        except:
            total_paid = 0
    else:
        total_paid = 0

    return render(request, 'providers/orders/edit.html', locals())
