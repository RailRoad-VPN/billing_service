import datetime
import logging
import sys
import uuid

from psycopg2._psycopg import DatabaseError

from app.exception import BillingError, PaymentException, PaymentNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class Payment(object):
    __version__ = 1

    _suuid = None
    _type_id = None
    _created_date = None

    def __init__(self, suuid: str = None, type_id: int = None, created_date: datetime = None):
        self._suuid = suuid
        self._type_id = type_id
        self._created_date = created_date

    def to_dict(self):
        return {
            'uuid': self._suuid,
            'type_id': self._type_id,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'uuid': self._suuid,
            'type_id': self._type_id,
            'created_date': self._created_date,
        }


class PaymentStored(StoredObject, Payment):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, type_id: int = None,
                 created_date: datetime = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        Payment.__init__(self, suuid=suuid, type_id=type_id, created_date=created_date)


class PaymentDB(PaymentStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _type_id_field = 'type_id'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find_by_id(self):
        logging.info('PaymentDB find_by_id method')
        select_sql = '''
                    SELECT
                        p.uuid AS uuid,
                        p.type_id AS type_id,
                        to_json(created_date) AS created_date
                    FROM public.payment p
                    WHERE p.uuid = ?
        '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (
            self._suuid
        )
        try:
            logging.debug('Call database service')
            payment_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.PAYMENT_FIND_ERROR_DB.message
            error_code = BillingError.PAYMENT_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PAYMENT_FIND_BY_ID_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise PaymentException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(payment_list_db) == 1:
            payment_db = payment_list_db[0]
        elif len(payment_list_db) == 0:
            error_message = BillingError.PAYMENT_FIND_BY_ID_ERROR.message
            error_code = BillingError.PAYMENT_FIND_BY_ID_ERROR.code
            developer_message = BillingError.PAYMENT_FIND_BY_ID_ERROR.developer_message
            raise PaymentNotFoundException(error=error_message, error_code=error_code,
                                           developer_message=developer_message)
        else:
            error_message = BillingError.PAYMENT_FIND_BY_ID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % BillingError.PAYMENT_FIND_BY_ID_ERROR.developer_message
            error_code = BillingError.PAYMENT_FIND_BY_ID_ERROR.code
            raise PaymentException(message=error_message, code=error_code, developer_message=developer_message)

        return self.__map_paymentdb_to_payment(payment_db=payment_db)

    def create(self):
        self._suuid = uuid.uuid4()
        logging.info('PaymentDB create method')
        insert_sql = '''INSERT INTO public.payment (uuid, type_id) VALUES (?, ?);'''
        insert_params = (
            self._suuid,
            self._type_id,
        )
        logging.debug('Create PaymentDB SQL : %s' % insert_sql)

        try:
            logging.debug('Call database service')
            self._storage_service.create(sql=insert_sql, data=insert_params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PAYMENT_CREATE_ERROR_DB.message
            error_code = BillingError.PAYMENT_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PAYMENT_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise PaymentException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('PaymentDB created.')

        return str(self._suuid)

    def update(self):
        logging.info('Payment update method')

        update_sql = '''
                    UPDATE public.payment 
                    SET
                        type_id = ?,
                        created_date = ?
                    WHERE 
                        uuid = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._type_id,
            self._created_date,
            self._suuid,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('Payment updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PAYMENT_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PAYMENT_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = BillingError.PAYMENT_UPDATE_ERROR_DB.code
            raise PaymentException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_paymentdb_to_payment(self, payment_db):
        return Payment(
            suuid=payment_db[self._suuid_field],
            type_id=payment_db[self._type_id_field],
            created_date=payment_db[self._created_date_field],
        )
