from instant2fa import errors
from instant2fa.api_requestor import APIRequestor
from instant2fa import jsonapi


class Instant2FAResource(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserAccessToken(Instant2FAResource):
    resource_type = 'user-access-tokens'

    @classmethod
    def create(cls, distinct_id, method='POST'):
        body = jsonapi.construct_request_body(
            cls.resource_type, distinct_id=distinct_id
        )
        path = jsonapi.construct_path(cls.resource_type, method)
        response = APIRequestor().request(
            method, path, body=body, accepted_codes=[201]
        )
        return cls(**jsonapi.get_attributes_from_response(response))


class VerificationRequest(Instant2FAResource):
    resource_type = 'verification-requests'

    @classmethod
    def handle_response(cls, response):
        if response.status_code == 422:
            raise errors.MFANotEnabled
        return cls(**jsonapi.get_attributes_from_response(response))

    @classmethod
    def create(cls, distinct_id, method='POST'):
        body = jsonapi.construct_request_body(
            cls.resource_type, distinct_id=distinct_id
        )
        path = jsonapi.construct_path(cls.resource_type, method)
        response = APIRequestor().request(
            method, path, body=body, accepted_codes=[201, 422]
        )
        return cls.handle_response(response)


class VerificationResponseToken(Instant2FAResource):
    resource_type = 'verification-response-tokens'

    @classmethod
    def retrieve(cls, token, method='GET'):
        path = jsonapi.construct_path(
            cls.resource_type, method, lookup_key=token
        )
        response = APIRequestor().request(method, path, accepted_codes=[202])
        return cls(**jsonapi.get_attributes_from_response(response))


def create_settings(distinct_id):
    """
    Args:
        distinct_id: string
    Returns:
        string: Hosted settings page URL

    """
    user_access_token = UserAccessToken.create(distinct_id)
    return user_access_token.hosted_page_url


def create_verification(distinct_id):
    """
    Args:
        distinct_id: string
    Returns:
        string: Hosted verification page URL
    """
    verification = VerificationRequest.create(distinct_id)
    return verification.hosted_page_url


def confirm_verification(distinct_id, token):
    """
    Args:
        distinct_id: string
        token: string
    Returns:
        boolean
    Raises:
        VerificationMismatch
        VerificationFailed
    """
    verification_response = VerificationResponseToken.retrieve(token)
    if verification_response.distinct_id != distinct_id:
        raise errors.VerificationMismatch(
            "The distinct_id passed back from the request didn't match the "
            "one passed into function. Are you passing in the right value for "
            "distinct_id?"
        )
    if verification_response.status != 'succeeded':
        raise errors.VerificationFailed(
            "The verification did not pass. The status was {}".
            format(verification_response.status)
        )
    return True
