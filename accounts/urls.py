
from django.conf.urls import url

from django.utils.translation import ugettext as _

from accounts.forms import SetPasswordFormEdited, AuthenticationFormEdited
from . import views

urlpatterns = [
                url(r'^message/(?P<code>[-\w]+)/$', views.message, name='message'),
                url(r'^profile/password/reset/$', views.password_reset, name='password_reset'),
                url(r'^login/$', views.login_view, name='login'),
                url(r'^logout/$', views.logout_view, name='logout'),
                # url(r'^login/$', 'django.contrib.auth.views.login', {
                #             'template_name': 'accounts/login.html',
                #             'authentication_form': AuthenticationFormEdited,
                #             'extra_context': {
                #                 'page': {
                #                     'title': _('Log in'),
                #                 },
                #             }
                #         }, name='login'),
                # # url(r'^logout/$', 'django.contrib.auth.views.logout', {
                #             'next_page': '/',
                #         }, name='logout'),
                # url(r'^profile/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                #             'django.contrib.auth.views.password_reset_confirm', {
                #                 'template_name': 'accounts/password_reset_confirm.html',
                #                 'set_password_form': SetPasswordFormEdited,
                #                 'post_reset_redirect': '/accounts/message/password_reset_confirm/',
                #             }, 'password_reset_confirm', ),
                ]
