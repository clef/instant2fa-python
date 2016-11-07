#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_instant2fa
----------------------------------

Tests for `instant2fa` module.
"""
import pytest
import requests
import requests_mock

import instant2fa
from instant2fa import errors

TOKEN_ID = 'tok_123'
DISTINCT_ID = 'A_UNIQUE_ID'

USER_ACCESS_TOKEN_URL = '{}/user-access-tokens/'.format(instant2fa.api_base)
VERIFICATION_REQUEST_URL = '{}/verification-requests/'.format(
    instant2fa.api_base
)
VERIFICATION_RESPONSE_TOKEN_URL = '{}/verification-response-tokens/tok_123'.format(
    instant2fa.api_base
)


@pytest.fixture
def user_access_token():
    return {
        'data': {
            'attributes': {
                'hosted_page_url': 'test_hosted_pages',
                'distinct_id': DISTINCT_ID
            },
            'type': 'user-access-tokens'
        }
    }


@pytest.fixture
def verification_request():
    return {
        'data': {
            'attributes': {
                'hosted_page_url': 'test_hosted_pages',
                'distinct_id': DISTINCT_ID
            },
            'type': 'verification-requests'
        }
    }


@pytest.fixture
def verification_response_token():
    return {
        'data': {
            'attributes': {
                'status': 'succeeded',
                'distinct_id': DISTINCT_ID
            },
            'type': 'verification-responses'
        }
    }


@pytest.fixture
def failed_verification_response_token():
    return {
        'data': {
            'attributes': {
                'status': 'failed',
                'distinct_id': DISTINCT_ID
            },
            'type': 'verification-responses'
        }
    }


@pytest.fixture
def error():
    return {
        'errors': [{
            "status": 400,
            "detail": "Something went wrong.",
            "title": "ValidationException"
        }]
    }


@pytest.fixture
def configured_instant2fa():
    instant2fa.access_key = 'ACCESS_KEY'
    instant2fa.access_secret = 'ACCESS_SECRET'
    return instant2fa


def test_authentication():
    instant2fa.access_key = None
    instant2fa.access_secret = None
    with pytest.raises(errors.AuthenticationError):
        instant2fa.create_settings(DISTINCT_ID)


def test_create_settings(configured_instant2fa, user_access_token):

    with requests_mock.Mocker() as mock:

        mock.request(
            'POST',
            USER_ACCESS_TOKEN_URL,
            json=user_access_token,
            status_code=201
        )
        hosted_pages_url = configured_instant2fa.create_settings(DISTINCT_ID)
        assert hosted_pages_url == 'test_hosted_pages'


def test_create_settings_error(configured_instant2fa, error):
    with requests_mock.Mocker() as mock:
        mock.request('POST', USER_ACCESS_TOKEN_URL, json=error, status_code=401)
        with pytest.raises(errors.APIError):
            configured_instant2fa.create_settings(DISTINCT_ID)


def test_create_verification(configured_instant2fa, verification_request):
    with requests_mock.Mocker() as mock:
        mock.request(
            'POST',
            VERIFICATION_REQUEST_URL,
            json=verification_request,
            status_code=201
        )
        hosted_pages_url = configured_instant2fa.create_verification(
            DISTINCT_ID
        )
        assert hosted_pages_url == 'test_hosted_pages'


def test_create_verification_for_non_mfa_enabled_user(
    configured_instant2fa, verification_request
):
    with requests_mock.Mocker() as mock:
        mock.request(
            'POST',
            VERIFICATION_REQUEST_URL,
            json=verification_request,
            status_code=422
        )
        with pytest.raises(errors.MFANotEnabled):
            configured_instant2fa.create_verification(DISTINCT_ID)


def test_confirm_verification(
    configured_instant2fa, verification_response_token
):
    with requests_mock.Mocker() as mock:
        mock.request(
            'GET',
            VERIFICATION_RESPONSE_TOKEN_URL,
            json=verification_response_token,
            status_code=202
        )
        confirmed = configured_instant2fa.confirm_verification(
            DISTINCT_ID, TOKEN_ID
        )
        assert confirmed


def test_confirm_verification_mismatch(
    configured_instant2fa, verification_response_token
):
    with requests_mock.Mocker() as mock:
        mock.request(
            'GET',
            VERIFICATION_RESPONSE_TOKEN_URL,
            json=verification_response_token,
            status_code=202
        )
        with pytest.raises(errors.VerificationMismatch):
            configured_instant2fa.confirm_verification(
                'mismatched_id', TOKEN_ID
            )


def test_confirm_verification_failed(
    configured_instant2fa, failed_verification_response_token
):
    with requests_mock.Mocker() as mock:
        mock.request(
            'GET',
            VERIFICATION_RESPONSE_TOKEN_URL,
            json=failed_verification_response_token,
            status_code=202
        )
        with pytest.raises(errors.VerificationFailed):
            configured_instant2fa.confirm_verification(DISTINCT_ID, TOKEN_ID)
