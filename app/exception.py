from enum import IntEnum

i = 0


def count():
    global i
    i += 1
    return i


class BillingError(IntEnum):
    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj

    UNKNOWN_ERROR_CODE = (i, 'UNKNOWN_ERROR_CODE phrase', 'UNKNOWN_ERROR_CODE description')

    REQUEST_NO_JSON = (count(), 'REQUEST_NO_JSON phrase', 'REQUEST_NO_JSON description')

    SUBSCRIPTION_FIND_ERROR_DB = (count(), 'SUBSCRIPTION_FIND_ERROR_DB phrase', 'SUBSCRIPTION_FIND_ERROR_DB description')
    FEATURE_FIND_ERROR_DB = (count(), 'FEATURE_FIND_ERROR_DB phrase', 'FEATURE_FIND_ERROR_DB description')

    BAD_ACCEPT_LANGUAGE_HEADER = (count(), 'BAD_ACCEPT_LANGUAGE_HEADER phrase', 'BAD_ACCEPT_LANGUAGE_HEADER description')


class BillingException(Exception):
    __version__ = 1

    error = None
    error_code = None
    developer_message = None

    def __init__(self, error: str, error_code: int, developer_message: str = None, *args):
        super().__init__(*args)
        self.error = error
        self.error_code = error_code
        self.developer_message = developer_message


class SubscriptionException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubscriptionNotFoundException(SubscriptionException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FeatureException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FeatureNotFoundException(FeatureException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
