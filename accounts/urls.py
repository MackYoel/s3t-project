from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from accounts.forms import SetPasswordFormEdited, AuthenticationFormEdited

urlpatterns = patterns('accounts.views',
                       url(r'^message/(?P<code>[-\w]+)/$', 'message', name='message'),
                       url(r'^profile/password/reset/$', 'password_reset', name='password_reset'),
                       )

urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^login/$', 'login', {
                            'template_name': 'accounts/login.html',
                            'authentication_form': AuthenticationFormEdited,
                            'extra_context': {
                                'page': {
                                    'title': _('Log in'),
                                },
                            }
                        }, name='login'),
                        url(r'^logout/$', 'logout', {
                            'next_page': '/',
                        }, name='logout'),
                        url(r'^profile/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                            'password_reset_confirm', {
                                'template_name': 'accounts/password_reset_confirm.html',
                                'set_password_form': SetPasswordFormEdited,
                                'post_reset_redirect': '/accounts/message/password_reset_confirm/',
                            }, 'password_reset_confirm', ),
                        )
