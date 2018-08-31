import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import BillingError, BillingException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class PaymentType(object):
    __version__ = 1

    _sid = None
    _name = None

    def __init__(self, sid: int = None, name: str = None):
        self._sid = sid
        self._name = name

    def to_dict(self):
        return {
            'id': self._sid,
            'name': self._name,
        }

    def to_api_dict(self):
        return {
            'id': self._sid,
            'name': self._name,
        }


class PaymentTypeStored(StoredObject, PaymentType):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, name: int = None, limit: int = None,
                 offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        PaymentType.__init__(self, sid=sid, name=name)


class PaymentTypeDB(PaymentTypeStored):
    __version__ = 1

    _sid_field = 'id'
    _name_field = 'name'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        self.logger.info('PaymentTypeDB find method')
        select_sql = '''
                      SELECT 
                        id,
                        name, 
                      FROM public.payment_type
                      '''
        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")

        try:
            self.logger.debug('Call database service')
            paymenttype_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.STATE_FIND_ERROR_DB.message
            error_code = BillingError.STATE_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    BillingError.STATE_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)
        paymenttype_list = []

        for paymenttype_db in paymenttype_list_db:
            paymenttype = self.__mappaymenttypedb_to_paymenttype(paymenttype_db)
            paymenttype_list.append(paymenttype)

        if len(paymenttype_list) == 0:
            logging.warning('Empty PaymentType list of method find. Very strange behaviour.')

        return paymenttype_list

    def __mappaymenttypedb_to_paymenttype(self, payment_type_db):
        return PaymentType(
            sid=payment_type_db[self._sid_field],
            name=payment_type_db[self._name_field],
        )
