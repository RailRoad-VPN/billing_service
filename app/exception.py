from enum import Enum

name = 'BILLING-'
i = 0


def count():
    global i
    i += 1
    return i


def get_all_error_codes():
    return [e.code for e in BillingError]


class BillingError(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, code, message, developer_message):
        self.code = code
        self.message = message
        self.developer_message = developer_message

    UNKNOWN_ERROR_CODE = (name + str(count()), 'UNKNOWN_ERROR_CODE phrase', 'UNKNOWN_ERROR_CODE description')

    REQUEST_NO_JSON = (name + str(count()), 'REQUEST_NO_JSON phrase', 'REQUEST_NO_JSON description')

    SUBSCRIPTION_FIND_ERROR_DB = (
    name + str(count()), 'SUBSCRIPTION_FIND_ERROR_DB phrase', 'SUBSCRIPTION_FIND_ERROR_DB description')
    FEATURE_FIND_ERROR_DB = (name + str(count()), 'FEATURE_FIND_ERROR_DB phrase', 'FEATURE_FIND_ERROR_DB description')
    USER_SUBSCRIPTION_FINDBYUUID_ERROR_DB = (name + str(count()), 'USER_SUBSCRIPTION_FINDBYUUID_ERROR_DB phrase',
                                             'USER_SUBSCRIPTION_FINDBYUUID_ERROR_DB description')
    USER_SUBSCRIPTION_FINDBYUUID_ERROR = (
    name + str(count()), 'USER_SUBSCRIPTION_FINDBYUUID_ERROR phrase', 'USER_SUBSCRIPTION_FINDBYUUID_ERROR description')

    BAD_ACCEPT_LANGUAGE_HEADER = (
    name + str(count()), 'BAD_ACCEPT_LANGUAGE_HEADER phrase', 'BAD_ACCEPT_LANGUAGE_HEADER description')


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


class UserSubscriptionException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserSubscriptionNotFoundException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
