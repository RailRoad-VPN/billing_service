import datetime
import sys

import logging

from psycopg2._psycopg import DatabaseError

from app.exception import BillingError, BillingException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class Payment(object):
    __version__ = 1

    _sid = None
    _type_id = None
    _created_date = None

    def __init__(self, sid: int = None, type_id: int = None, created_date: datetime = None):
        self._sid = sid
        self._type_id = type_id
        self._created_date = created_date

    def to_dict(self):
        return {
            'id': self._sid,
            'type_id': self._type_id,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'id': self._sid,
            'type_id': self._type_id,
            'created_date': self._created_date,
        }


class PaymentStored(StoredObject, Payment):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, type_id: int = None,
                 created_date: datetime = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        Payment.__init__(self, sid=sid, type_id=type_id, created_date=created_date)


class PaymentDB(PaymentStored):
    __version__ = 1

    _sid_field = 'id'
    _type_id_field = 'type_id'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def create(self):
        logging.info('PaymentDB create method')
        insert_sql = '''
                      INSERT INTO public.payment 
                        (type_id, created_date) 
                      VALUES 
                        (?, ?)
                      RETURNING id;
                     '''
        insert_params = (
            self._type_id,
            self._created_date,
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
                                    BillingError.PAYMENT_CREATE_ERROR_DB.description, e.pgcode, e.pgerror)

            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('PaymentDB created.')

        return self._sid

    def update(self):
        logging.info('Payment update method')

        update_sql = '''
                    UPDATE public.payment 
                    SET
                        type_id = ?,
                        created_date = ?
                    WHERE 
                        id = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._type_id,
            self._created_date,
            self._sid,
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
                                    BillingError.PAYMENT_UPDATE_ERROR_DB.description, e.pgcode, e.pgerror)
            error_code = BillingError.PAYMENT_UPDATE_ERROR_DB.code
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __mappaymentdb_to_payment(self, payment_db):
        return Payment(
            sid=payment_db[self._sid_field],
            type_id=payment_db[self._type_id_field],
            created_date=payment_db[self._created_date_field],
        )
