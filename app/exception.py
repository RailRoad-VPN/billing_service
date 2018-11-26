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
    BAD_IDENTITY_ERROR = (name + str(count()), 'BAD_IDENTITY_ERROR phrase', 'BAD_IDENTITY_ERROR description')

    Service_FIND_ERROR_DB = (name + str(count()), 'Service_FIND_ERROR_DB phrase', 'Service_FIND_ERROR_DB description')

    FEATURE_FIND_ERROR_DB = (name + str(count()), 'FEATURE_FIND_ERROR_DB phrase', 'FEATURE_FIND_ERROR_DB description')

    USER_RRNSERVICE_FIND_BY_UUID_ERROR_DB = (name + str(count()), 'USER_RRNSERVICE_FIND_BY_UUID_ERROR_DB phrase', 'USER_RRNSERVICE_FIND_BY_UUID_ERROR_DB description')
    USER_RRNSERVICE_FIND_BY_UUID_ERROR = (name + str(count()), 'USER_RRNSERVICE_FIND_BY_UUID_ERROR phrase', 'USER_RRNSERVICE_FIND_BY_UUID_ERROR description')
    USER_RRNSERVICE_FIND_BY_USER_UUID_ERROR_DB = (name + str(count()), 'USER_RRNSERVICE_FIND_BY_USER_UUID_ERROR_DB phrase', 'USER_RRNSERVICE_FIND_BY_USER_UUID_ERROR_DB description')
    USER_RRNSERVICE_FIND_BY_USER_UUID_ERROR = (name + str(count()), 'USER_RRNSERVICE_FIND_BY_USER_UUID_ERROR phrase', 'USER_RRNSERVICE_FIND_BY_USER_UUID_ERROR description')
    USER_RRNSERVICE_NOT_FOUND_ERROR = (name + str(count()), 'USER_RRNSERVICE_NOT_FOUND_ERROR phrase', 'USER_RRNSERVICE_NOT_FOUND_ERROR description')
    USER_RRNSERVICE_UPDATE_ERROR_DB = (name + str(count()), 'USER_RRNSERVICE_UPDATE_ERROR_DB phrase', 'USER_RRNSERVICE_UPDATE_ERROR_DB description')
    USER_RRNSERVICE_CREATE_ERROR_DB = (name + str(count()), 'USER_RRNSERVICE_CREATE_ERROR_DB phrase', 'USER_RRNSERVICE_CREATE_ERROR_DB description')

    PAYMENT_FIND_ERROR_DB = (name + str(count()), 'PAYMENT_FIND_ERROR_DB phrase', 'PAYMENT_FIND_ERROR_DB description')
    PAYMENT_FIND_BY_ID_ERROR_DB = (name + str(count()), 'PAYMENT_FIND_BY_ID_ERROR_DB phrase', 'PAYMENT_FIND_BY_ID_ERROR_DB description')
    PAYMENT_CREATE_ERROR_DB = (name + str(count()), 'PAYMENT_CREATE_ERROR_DB phrase', 'PAYMENT_CREATE_ERROR_DB description')
    PAYMENT_UPDATE_ERROR_DB = (name + str(count()), 'PAYMENT_UPDATE_ERROR_DB phrase', 'PAYMENT_UPDATE_ERROR_DB description')
    PAYMENT_FIND_BY_ID_ERROR = (name + str(count()), 'PAYMENT_FIND_BY_ID_ERROR phrase', 'PAYMENT_FIND_BY_ID_ERROR description')

    SERVICE_FIND_ERROR_DB = (name + str(count()), 'SERVICE_FIND_ERROR_DB phrase', 'SERVICE_FIND_ERROR_DB description')

    ORDER_CREATE_ERROR_DB = (name + str(count()), 'ORDER_CREATE_ERROR_DB phrase', 'ORDER_CREATE_ERROR_DB description')
    ORDER_UPDATE_ERROR_DB = (name + str(count()), 'ORDER_UPDATE_ERROR_DB phrase', 'ORDER_UPDATE_ERROR_DB description')
    ORDER_FIND_BY_CODE_ERROR = (name + str(count()), 'ORDER_FIND_BY_CODE_ERROR phrase', 'ORDER_FIND_BY_CODE_ERROR description')
    ORDER_FIND_BY_CODE_ERROR_DB = (name + str(count()), 'ORDER_FIND_BY_CODE_ERROR_DB phrase', 'ORDER_FIND_BY_CODE_ERROR_DB description')
    ORDER_FIND_BY_UUID_ERROR_DB = (name + str(count()), 'ORDER_FIND_BY_ID_ERROR_DB phrase', 'ORDER_FIND_BY_ID_ERROR_DB description')
    ORDER_FIND_BY_UUID_ERROR = (name + str(count()), 'ORDER_FIND_BY_ID_ERROR phrase', 'ORDER_FIND_BY_ID_ERROR description')
    ORDER_FIND_ERROR_DB = (name + str(count()), 'ORDER_FIND_ERROR_DB phrase', 'ORDER_FIND_ERROR_DB description')
    ORDER_IDENTIFIER_ERROR = (name + str(count()), 'ORDER_IDENTIFIER_ERROR phrase', 'ORDER_IDENTIFIER_ERROR description')
    ORDER_UPDATE_IDENTIFIER_ERROR = (name + str(count()), 'ORDER_UPDATE_IDENTIFIER_ERROR phrase', 'ORDER_UPDATE_IDENTIFIER_ERROR description')
    ORDER_CREATE_CODE_EXIST_ERROR = (name + str(count()), 'ORDER_CREATE_CODE_EXIST_ERROR phrase', 'ORDER_CREATE_CODE_EXIST_ERROR description')
    ORDER_UPDATE_CODE_EXIST_ERROR = (name + str(count()), 'ORDER_UPDATE_CODE_EXIST_ERROR phrase', 'ORDER_UPDATE_CODE_EXIST_ERROR description')
    ORDER_UPDATE_NOT_EXIST_ERROR = (name + str(count()), 'ORDER_UPDATE_NOT_EXIST_ERROR phrase', 'ORDER_UPDATE_NOT_EXIST_ERROR description')

    BAD_ACCEPT_LANGUAGE_HEADER = (name + str(count()), 'BAD_ACCEPT_LANGUAGE_HEADER phrase', 'BAD_ACCEPT_LANGUAGE_HEADER description')

    ORDERPAYMENT_FIND_ERROR_DB = (name + str(count()), 'ORDERPAYMENT_FIND_ERROR_DB phrase', 'ORDERPAYMENT_FIND_ERROR_DB description')
    ORDERPAYMENT_FIND_BY_PAYMENT_ERROR_DB = (name + str(count()), 'ORDERPAYMENT_FIND_BY_PAYMENT_ERROR_DB phrase', 'ORDERPAYMENT_FIND_BY_PAYMENT_ERROR_DB description')
    ORDERPAYMENT_FIND_BY_PAYMENT_ERROR = (name + str(count()), 'ORDERPAYMENT_FIND_BY_PAYMENT_ERROR phrase', 'ORDERPAYMENT_FIND_BY_PAYMENT_ERROR description')
    ORDERPAYMENT_FIND_BY_ORDER_ERROR_DB = (name + str(count()), 'ORDERPAYMENT_FIND_BY_ORDER_ERROR_DB phrase', 'ORDERPAYMENT_FIND_BY_ORDER_ERROR_DB description')
    ORDERPAYMENT_CREATE_ERROR_DB = (name + str(count()), 'ORDERPAYMENT_CREATE_ERROR_DB phrase', 'ORDERPAYMENT_CREATE_ERROR_DB description')


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


class RRNServiceException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RRNServiceNotFoundException(RRNServiceException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PaymentException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PaymentNotFoundException(PaymentException):
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


class OrderPaymentException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OrderPaymentNotFoundException(OrderPaymentException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PPGPaymentException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PPGPaymentNotFoundException(PPGPaymentException):
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


class UserRRNServiceException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserRRNServiceNotFoundException(BillingException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
