"""
WSGI config for XemaCars_ECommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import stripe

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "XemaCars_ECommerce.settings")

stripe.api_key = settings.STRIPE_SECRET_KEY
application = get_wsgi_application()
