class Instant2FAError(Exception):
    pass


class APIError(Instant2FAError):
    pass


class AuthenticationError(Instant2FAError):
    pass


class MFANotEnabled(Instant2FAError):
    pass


class VerificationMismatch(Instant2FAError):
    pass


class VerificationFailed(Instant2FAError):
    pass

