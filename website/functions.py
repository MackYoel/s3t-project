import sendgrid
from sendgrid.helpers.mail import *

from bitheart.settings import SENDGRID_KEY



def send_email(from_name, from_email, to_email, subject, text_content, html_content, attachment=None):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_KEY)
    mail = Mail(to_email=Email(to_email),
                from_email=Email(from_email, from_name),
                subject=subject,
                content=Content("text/plain", text_content))

    mail.add_content(Content("text/html", html_content))

    if attachment is not None and isinstance(attachment, Attachment):
        mail.add_attachment(attachment)

    data = mail.get()
    sg.client.mail.send.post(request_body=data)
    return True


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
