import django_heroku
import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from .base import *


DEBUG = False
django_heroku.settings(locals())
sentry_sdk.init(
    dsn="https://87e33741581f4681a2ac41266d6aa73f@sentry.io/1337071",
    integrations=[DjangoIntegration()]
)
