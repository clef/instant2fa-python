# -*- coding: utf-8 -*-
# Instant2FA Python bindings
# API docs at https://docs.instant2fa.com/

__author__ = 'Grace Wong'
__email__ = 'grace@getclef.com'
__version__ = '1.0.0'

api_base = 'https://api.instant2fa.com'
access_key = None
access_secret = None

from instant2fa.resources import (
    create_settings,
    create_verification,
    confirm_verification
)
