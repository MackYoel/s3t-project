import time
from uuid import uuid4

import sendgrid
from sendgrid.helpers.mail import *

from s3t.settings import SENDGRID_KEY


def send_email(subject=None, from_email=None, to_email=None, content=None):
    """Returns the error (string) if there is any, None otherwise"""
    if SENDGRID_KEY is None:
        return 'SENDGRID_KEY is not setted up.'
    if None in (subject, from_email, to_email, content):
        return 'subject, from_email, to_email, content are required.'

    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_KEY)
    mail = Mail(
        Email(from_email),
        subject,
        Email(to_email),
        Content("text/html", content)
    )
    try:
        resp = sg.client.mail.send.post(request_body=mail.get())
    except Exception as err:
        return err

    if resp.status_code == 202:
        return None
    return resp.body


def add_form_control_class(fields):
    for f in fields:
        fields[f].widget.attrs.update({'class': 'form-control'})


def add_form_control_datepicker_class(form, fields):
    for f in fields:
        form.fields[f].widget.attrs.update({'class': 'form-control datepicker'})


def add_form_text(form, fields):
    for f in fields:
        form.fields[f].widget.attrs.update({'type': 'text'})


def add_form_onlyread(form, fields):
    for f in fields:
        form.fields[f].widget.attrs.update({'readonly': 'true'})


def add_form_required(fields):
    for f in fields:
        fields[f].widget.attrs.update({'required': 'true'})


def update_form_labels(form, fields):
    for f in fields:
        form.fields[f].label = fields[f]


def create_unique_token():
    return '{}-{}'.format(uuid4(), time.time())


class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return ''

    def decrement(self):
        self.count -= 1
        return ''

    def double(self):
        self.count *= 2
        return ''