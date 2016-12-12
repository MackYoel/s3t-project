# coding=utf-8

from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from accounts.forms import PersonForm
from accounts.models import Person
from main.forms import OrderReceivedForm, PaymentForm
from main.functions import send_email, create_unique_token, json, Counter
from main.models import Product, CarSession, Order, OrderItem, Payment
from s3t.settings import DOMAIN_NAME, FROM_EMAIL, EMAIL_SUBJECT_ORDER, EMAIL_BODY_ORDER, FROM_NAME


@login_required()
def panel(request):
    return render(request, 'main/panel.html')


@login_required()
def provider_list(request):
    providers = Person.objects.filter(is_staff=False)
    return render(request, 'main/providers/list.html', locals())


@login_required()
def provider_new(request):
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
                return redirect(reverse('provider_list'))
            return HttpResponse("""
                <script>
                    alert("ha ocurrido un error enviando el correo al proveedor");
                    window.location.href = '%s';
                </script>""" % reverse('providers'))
    else:
        title = 'Nuevo Proveedor'
        form = PersonForm()

    comeback_to = 'provider_list'
    return render(request, 'hook/form_layout.html', locals())


@login_required()
def provider_edit(request, pk):
    provider = get_object_or_404(Person, pk=int(pk))
    title = 'Editar Proveedor'
    comeback_to = 'provider_list'

    if request.method == 'POST' and request.POST:
        form = PersonForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect(reverse('provider_list'))
        else:
            return render(request, 'hook/form_layout.html', locals())

    form = PersonForm(instance=provider)
    return render(request, 'hook/form_layout.html', locals())


@login_required()
@staff_member_required
def car(request):
    provider_pk = int(request.GET.get('provider', 0))
    if provider_pk > 0:
        _provider = get_object_or_404(Person, pk=provider_pk)
        products = Product.objects.filter(provider=_provider)
    else:
        products = Product.objects.all()
    title = 'Tienda de Productos'
    providers = Person.objects.filter(is_staff=False)
    products_in_car = CarSession.objects.filter(user=request.user)

    print(provider_pk)
    # print(provider_pk+1)
    return render(request, 'main/car/product_list.html', locals())


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
                CarSession.objects.create(user=request.user, product=product, provider=product.provider)
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
@csrf_exempt
def car_update_product(request):
    result = {}
    if request.method == 'POST':
        product_pk = int(request.POST.get('product_pk', 0))
        quantity = int(request.POST.get('quantity', 0))
        note = request.POST.get('note', None)

        product = get_object_or_404(Product, pk=product_pk)
        if product:
            try:
                car_session = CarSession.objects.get(user=request.user, product=product)
                if quantity > 0:
                    car_session.quantity = quantity
                if note:
                    car_session.note = note
                car_session.save()
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
def car_update_order(request):
    title = 'Tienda de Productos, actualización de cantidades'
    providers = CarSession.objects.values('provider').distinct()
    if providers.count() == 0:
        return redirect(reverse('car'))

    products_in_car_by_provider = list()
    for p in providers:
        provider = Person.objects.get(pk=p['provider'])
        products_in_car_by_provider.append((
            {'provider': provider.get_full_name(), 'products_in_car': CarSession.objects.filter(user=request.user,
                                                                                                provider=p[
                                                                                                    'provider'])}))
    counter = Counter()
    return render(request, 'main/car/update_quantity.html', locals())


@login_required()
@staff_member_required
def car_create_orders(request):
    providers = CarSession.objects.values('provider').distinct()

    message = 'Se han enviado las ordenes de pedido a los proveedores'
    message += '<ul>'
    for p in providers:
        provider = Person.objects.get(pk=p['provider'])
        car_session_by_provider = CarSession.objects.filter(user=request.user, provider=p['provider'])
        order = Order.objects.create(provider=provider)
        for c in car_session_by_provider:
            subtotal = c.quantity * c.product.price
            OrderItem.objects.create(product=c.product, quantity=c.quantity, observation=c.observation,
                                     total=subtotal, order=order, note=c.note)
            order.sub_total += subtotal
            order.total += subtotal
            order.quantity += c.quantity
            car_session_by_provider.delete()

        order.save()

        body = EMAIL_BODY_ORDER
        body = body.replace('[PROVIDER_NAME]', provider.get_full_name())
        body = body.replace('[FROM_NAME]', FROM_NAME)
        body = body.replace('[URL]', DOMAIN_NAME + reverse('providers:order_edit', kwargs={'pk': order.pk}))
        send_email(subject=EMAIL_SUBJECT_ORDER, content=body, to_email=provider.email)

        message += '<li>' + provider.get_full_name() + '</li>'
    message += '</ul>'
    return render(request, 'main/echo.html', locals())


@login_required()
@staff_member_required
def order_list(request):
    state = int(request.GET.get('state', -1))
    provider_pk = int(request.GET.get('provider', 0))
    if state > -1:
        orders = Order.objects.filter(state=state).order_by('-created_at')
    else:
        orders = Order.objects.all().order_by('-created_at')

    if provider_pk > 0:
        orders = orders.filter(provider__id=provider_pk)

    for o in orders:
        o.state_text = o.get_state_display()
        if o.state == Order.PAID:
            o.row_class = 'active'
        if o.state == Order.SENT:
            o.row_class = 'success'
            # o.state_text = 'Enviado por el proveedor'

    states = Order.ORDER_STATES
    providers = Person.objects.filter(is_staff=False)
    # if o.state == Order.
    return render(request, 'main/orders/list.html', locals())


@login_required()
@staff_member_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    title = 'Pedido a ' + order.provider.get_full_name()
    order_items = OrderItem.objects.filter(order=order)
    form = None

    if request.POST:
        if request.POST.get('check_received_at', False):
            order.received_at = datetime.now()
            order.state = Order.RECEIVED
        if request.POST.get('check_checked_at', False):
            form = OrderReceivedForm(request.POST, instance=order)
            if form.is_valid():
                order = form.save(commit=False)
                order.checked_at = datetime.now()
                order.state = Order.CHECKED
        if request.POST.get('check_paid_at', False):
            total_paid = Payment.objects.filter(order=order).aggregate(total_amount=Sum('amount'))
            if total_paid:
                total_paid = total_paid['total_amount']
                try:
                    total_paid = float(total_paid)
                except:
                    total_paid = 0
            else:
                total_paid = 0

            if order.total > total_paid:
                form = PaymentForm(request.POST, request.FILES)
                if form.is_valid():
                    payment = form.save(commit=False)
                    payment.order = order
                    payment.save()

                    total_paid += payment.amount
                    if total_paid - order.total == 0:
                        order.paid_at = datetime.now()
                        order.state = Order.PAID

        order.save()

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


    if order.sent_at:
        if not order.paid_at:
            next_action = 'check_paid_at'
            next_action_text = 'Marcar como Pagado'
            save_text = next_action_text
        if not order.checked_at:
            next_action = 'check_checked_at'
            next_action_text = 'Marcar como Revisado'
            save_text = next_action_text
        if not order.received_at:
            next_action = 'check_received_at'
            next_action_text = 'Marcar como Recibido'

        if order.state == Order.CHECKED:
            show_form = True
            form_title = 'Pago realizado'

            amount_to_pay = order.total - total_paid
            if amount_to_pay > 0:
                form = PaymentForm(initial={'amount': amount_to_pay})

        if order.state == Order.RECEIVED:
            show_form = True
            form_title = 'Revisión'
            form = OrderReceivedForm(instance=order)

    return render(request, 'main/orders/edit.html', locals())
