from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

from accounts.forms import PasswordResetFormEdited, AuthenticationFormEdited
from s3t.settings import DEFAULT_EMAIL, FROM_NAME, LOGIN_REDIRECT_URL
from website.functions import send_email


def message(request, code):
    if code == 'password_reset':
        message = _(
            '<strong>We have sent you an email!</strong> Please, follow the instructions to reset your password.')
        # messages.add_message(request, messages.INFO, message)
        return render(request, 'accounts/echo.html', locals())
        # return redirect(reverse('accounts:password_reset'))

    if code == 'password_reset_confirm':
        messages.add_message(request, messages.INFO, _(
            '<strong>Success!</strong> You have changed your password.'))
        return redirect(reverse('accounts:login'))

    if code == 'password_change_done':
        messages.add_message(request, messages.INFO, _(
            '<strong>Success!</strong> You have changed your password.'))
        return redirect(reverse('accounts:password_change'))

    return redirect(reverse('accounts:profile_edit'))


@csrf_protect
def password_reset(request):
    title = _('Reset password')
    from_email = 'no-reply@oneventus.com'
    domain = get_current_site(request)
    site_name = get_current_site(request)
    contact_email = DEFAULT_EMAIL
    # TODO put like setting value

    if request.method == "POST":
        form = PasswordResetFormEdited(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data["email"]
                user = User.objects.get(email__iexact=email)
                context = {
                    'email': user.email,
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                    'main_email': contact_email,
                }

                text_content = get_template('accounts/email/email_reset.html').render(context)
                html_content = get_template('accounts/email/email_reset.html').render(context)

                subject = loader.render_to_string('registration/password_reset_subject.txt', context)
                subject = ''.join(subject.splitlines())

                send_email(FROM_NAME, DEFAULT_EMAIL, email, subject, text_content, html_content)
                return HttpResponseRedirect('/accounts/message/password_reset/')

            except User.DoesNotExist:
                message = _('user not found')
    else:
        form = PasswordResetFormEdited()

    return render(request, 'accounts/password_reset.html', locals())


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(LOGIN_REDIRECT_URL)
        form = AuthenticationFormEdited(initial={'username': username})
    else:
        form = AuthenticationFormEdited()
    return render(request, 'accounts/login.html', locals())


def logout_view(request):
    logout(request)
    return redirect(LOGIN_REDIRECT_URL)
