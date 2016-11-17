from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import PersonForm
from accounts.models import Person
from django.urls import reverse
from django.http import HttpResponse
from website.functions import send_email, create_unique_token
from accounts.functions import generate_username
from s3t.settings import DOMAIN_NAME
from django.contrib.auth.decorators import login_required


@login_required()
def panel(request):
    return render(request, 'website/panel.html')


def providers(request):
    providers = Person.objects.all()
    return render(request, 'website/providers/list.html', locals())


def new_provider(request):
    if request.method == 'POST' and request.POST:
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person = generate_username(person.first_name)
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
    # if is_provider:
    return render(request, 'website/products/provider_list.html')
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
    pass
