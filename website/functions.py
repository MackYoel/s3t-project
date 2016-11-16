import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail
from s3t.settings import SEND_GRID_API_KEY
from uuid import uuid4
import time
# import sendgrid
# from sendgrid.helpers.mail import *

# from bitheart.settings import SENDGRID_KEY



# def send_email(from_name, from_email, to_email, subject, text_content, html_content, attachment=None):
#     sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_KEY)
#     mail = Mail(to_email=Email(to_email),
#                 from_email=Email(from_email, from_name),
#                 subject=subject,
#                 content=Content("text/plain", text_content))

#     mail.add_content(Content("text/html", html_content))

#     if attachment is not None and isinstance(attachment, Attachment):
#         mail.add_attachment(attachment)

#     data = mail.get()
#     sg.client.mail.send.post(request_body=data)
#     return True


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


def send_email(subject=None, from_email=None, to_email=None, content=None):
    """Returns the error (string) if there is any, None otherwise"""
    if SEND_GRID_API_KEY is None:
        return 'SEND_GRID_API_KEY is not setted up.'
    if None in (subject, from_email, to_email, content):
        return 'subject, from_email, to_email, content are required.'

    sg = sendgrid.SendGridAPIClient(apikey=SEND_GRID_API_KEY)
    mail = Mail(
        Email(from_email),
        subject,
        Email(to_email),
        Content("text/html", content)
    )
    try:
        resp = sg.client.mail.send.post(request_body=mail.get())
    except Exception as err:
        from toctochi_stereo import pprint
        pprint(err, label='err')
        return err

    if resp.status_code == 202:
        return None
    return resp.body


def create_unique_token():
    return '{}-{}'.format(uuid4(), time.time())
