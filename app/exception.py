import sys

sys.path.insert(0, '../rest_api_library')
from response import APIErrorEnum

name = 'BILLING-'
i = 0


def count():
    global i
    i += 1
    return i


def get_all_error_codes():
    return [e.code for e in BillingError]


class BillingError(APIErrorEnum):
    __version__ = 1

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    UNKNOWN_ERROR_CODE = (name + str(count()), 'UNKNOWN_ERROR_CODE phrase', 'UNKNOWN_ERROR_CODE description')

    REQUEST_NO_JSON = (name + str(count()), 'REQUEST_NO_JSON phrase', 'REQUEST_NO_JSON description')

    SUBSCRIPTION_FIND_ERROR_DB = (name + str(count()), 'SUBSCRIPTION_FIND_ERROR_DB phrase', 'SUBSCRIPTION_FIND_ERROR_DB description')

    FEATURE_FIND_ERROR_DB = (name + str(count()), 'FEATURE_FIND_ERROR_DB phrase', 'FEATURE_FIND_ERROR_DB description')

    USER_SUBSCRIPTION_FIND_BY_UUID_ERROR_DB = (name + str(count()), 'USER_SUBSCRIPTION_FIND_BY_UUID_ERROR_DB phrase', 'USER_SUBSCRIPTION_FIND_BY_UUID_ERROR_DB description')
    USER_SUBSCRIPTION_FIND_BY_UUID_ERROR = (name + str(count()), 'USER_SUBSCRIPTION_FIND_BY_UUID_ERROR phrase', 'USER_SUBSCRIPTION_FIND_BY_UUID_ERROR description')
    USER_SUBSCRIPTION_FIND_BY_USER_UUID_ERROR_DB = (name + str(count()), 'USER_SUBSCRIPTION_FIND_BY_USER_UUID_ERROR_DB phrase', 'USER_SUBSCRIPTION_FIND_BY_USER_UUID_ERROR_DB description')
    USER_SUBSCRIPTION_FIND_BY_USER_UUID_ERROR = (name + str(count()), 'USER_SUBSCRIPTION_FIND_BY_USER_UUID_ERROR phrase', 'USER_SUBSCRIPTION_FIND_BY_USER_UUID_ERROR description')

    PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR_DB = (name + str(count()), 'PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR_DB phrase', 'PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR_DB description')
    PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR = (name + str(count()), 'PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR phrase', 'PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR description')
    PPG_PAYMENT_FIND_BY_ORDERID_ERROR_DB = (name + str(count()), 'PPG_PAYMENT_FIND_BY_ORDERID_ERROR_DB phrase', 'PPG_PAYMENT_FIND_BY_ORDERID_ERROR_DB description')
    PPG_PAYMENT_FIND_BY_ORDERID_ERROR = (name + str(count()), 'PPG_PAYMENT_FIND_BY_ORDERID_ERROR phrase', 'PPG_PAYMENT_FIND_BY_ORDERID_ERROR description')

    ORDER_CREATE_ERROR_DB = (name + str(count()), 'ORDER_CREATE_ERROR_DB phrase', 'ORDER_CREATE_ERROR_DB description')
    ORDER_UPDATE_ERROR_DB = (name + str(count()), 'ORDER_UPDATE_ERROR_DB phrase', 'ORDER_UPDATE_ERROR_DB description')
    ORDER_FIND_BY_ID_ERROR_DB = (name + str(count()), 'ORDER_FIND_BY_ID_ERROR_DB phrase', 'ORDER_FIND_BY_ID_ERROR_DB description')
    ORDER_FIND_BY_ID_ERROR = (name + str(count()), 'ORDER_FIND_BY_ID_ERROR phrase', 'ORDER_FIND_BY_ID_ERROR description')
    ORDER_FIND_ERROR_DB = (name + str(count()), 'ORDER_FIND_ERROR_DB phrase', 'ORDER_FIND_ERROR_DB description')
    ORDER_IDENTIFIER_ERROR = (name + str(count()), 'ORDER_IDENTIFIER_ERROR phrase', 'ORDER_IDENTIFIER_ERROR description')

    BAD_ACCEPT_LANGUAGE_HEADER = (name + str(count()), 'BAD_ACCEPT_LANGUAGE_HEADER phrase', 'BAD_ACCEPT_LANGUAGE_HEADER description')


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


class BillingNotFoundException(Exception):
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


class OrderException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OrderNotFoundException(OrderException):
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
