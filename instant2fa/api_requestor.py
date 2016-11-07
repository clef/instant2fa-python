import json
from urlparse import urljoin

import requests

import instant2fa
from instant2fa import errors
from instant2fa import jsonapi

class APIRequestor(object):

    def __init__(
        self, access_key=None, access_secret=None, api_base=None, headers=None
    ):
        self.api_base = api_base or instant2fa.api_base
        self.access_key = access_key or instant2fa.access_key
        self.access_secret = access_secret or instant2fa.access_secret
        self.headers = headers or jsonapi.get_headers()

    def request(self, method, path, body=None, accepted_codes=None):
        if not self.access_key:
            raise errors.AuthenticationError(
                'No access key provided. (HINT: set your access key using '
                '"instant2fa.access_key = <ACCESS_KEY>"). You can generate '
                'access keys from the Instant2FA dashboard. '
                'See https://dashboard.instant2fa.com/login'
            )

        if not self.access_secret:
            raise errors.AuthenticationError(
                'No access secret provided. (HINT: set your access secret '
                'using "instant2fa.access_secret = <ACCESS_SECRET>"). You can '
                'generate  access secrets from the Instant2FA dashboard. '
                'See https://dashboard.instant2fa.com/login'
            )
        accepted_codes = accepted_codes or []
        uri = urljoin(self.api_base, path)
        auth = (self.access_key, self.access_secret)
        response = requests.request(
            method,
            uri,
            data=json.dumps(body),
            auth=auth,
            headers=self.headers
        )
        if response.status_code in accepted_codes:
            return response
        else:
            return self.handle_api_error(response)

    def handle_api_error(self, response):
        try:
            response.json()
        except ValueError:
            raise errors.APIError(
                "Invalid response object from API. HTTP response code "
                "was {}".format(response.status_code)
            )
        raise errors.APIError(jsonapi.get_error_from_response(response))
