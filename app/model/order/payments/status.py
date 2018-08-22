import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import BillingError, BillingException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class PaymentStatus(object):
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


class PaymentStatusStored(StoredObject, PaymentStatus):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, name: int = None, limit: int = None,
                 offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        PaymentStatus.__init__(self, sid=sid, name=name)


class PaymentStatusDB(PaymentStatusStored):
    __version__ = 1

    _sid_field = 'id'
    _name_field = 'name'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        self.logger.info('PaymentStatus find method')
        select_sql = '''
                      SELECT 
                        id,
                        name
                      FROM public.payment_status
                      '''
        self.logger.debug(f"Select SQL: {select_sql}")

        try:
            self.logger.debug('Call database service')
            payment_status_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.PAYMENTSTATUS_FIND_ERROR_DB.message
            error_code = BillingError.PAYMENTSTATUS_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    BillingError.PAYMENTSTATUS_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)
        payment_status_list = []

        for payment_status_db in payment_status_list_db:
            payment_status = self.__map_payment_statusdb_to_payment_status(payment_status_db)
            payment_status_list.append(payment_status)

        if len(payment_status_list) == 0:
            logging.warning('Empty PaymentStatus list of method find. Very strange behaviour.')

        return payment_status_list

    def __map_payment_statusdb_to_payment_status(self, payment_status_db):
        return PaymentStatus(
            sid=payment_status_db[self._sid_field],
            name=payment_status_db[self._name_field],
        )
