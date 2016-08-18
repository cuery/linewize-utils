from flask import render_template
from flask_mail import Mail, Message
import time


class MailSenderException(Exception):
    pass


class MailSender(object):
    __application_context = None
    __mail_object = None

    def __init__(self, application_context=None):
        if application_context is not None:
            MailSender.setContext(application_context)

    @staticmethod
    def setContext(application_context):
        MailSender.__application_context = application_context
        MailSender.__mail_object = Mail(application_context)

    @staticmethod
    def sendMail(template, recipients, subject, nosmtp=False, **keyword_arguments):
        if keyword_arguments is None:
            keyword_arguments = dict()
        keyword_arguments['servertime'] = time.strftime("%c UTC", time.gmtime())
        if MailSender.__mail_object is not None:
            msg = Message(recipients=recipients, subject=subject)
            msg.html = render_template(template, **keyword_arguments)
            if nosmtp:
                return msg
            else:
                MailSender.__mail_object.send(msg)
        else:
            raise MailSenderException("Application context is not loaded. Load it first using MailSender.setContext()")

    @staticmethod
    def send_raw_mail(recipients, subject, content, html):
        if MailSender.__mail_object is not None:
            msg = Message(recipients=recipients, subject=subject)

            if html:
                msg.html = content
            else:
                msg.body = content
            MailSender.__mail_object.send(msg)
        else:
            raise MailSenderException("Application context is not loaded. Load it first using MailSender.setContext()")
