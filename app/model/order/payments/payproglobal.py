import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import BillingError, PPGPaymentException, PPGPaymentNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class PayProGlobalPayment(object):
    __version__ = 1

    _sid = None
    _payment_suuid = None
    _order_id = None
    _json_data = None
    _created_date = None

    def __init__(self, sid: int = None, payment_suuid: str = None, order_id: int = None, json_data: str = None,
                 created_date: datetime = None):
        self._sid = sid
        self._payment_suuid = payment_suuid
        self._order_id = order_id
        self._json_data = json_data
        self._created_date = created_date

    def to_dict(self):
        return {
            'id': self._sid,
            'payment_uuid': str(self._payment_suuid),
            'order_id': self._order_id,
            'json_data': self._json_data,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'id': self._sid,
            'payment_uuid': str(self._payment_suuid),
            'order_id': self._order_id,
            'json_data': self._json_data,
            'created_date': self._created_date,
        }


class PayProGlobalPaymentStored(StoredObject, PayProGlobalPayment):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, payment_suuid: str = None,
                 order_id: int = None,
                 json_data: str = None, created_date: datetime = None,
                 limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        PayProGlobalPayment.__init__(self, sid=sid, payment_suuid=payment_suuid, order_id=order_id, json_data=json_data,
                                     created_date=created_date, )


class PayProGlobalPaymentDB(PayProGlobalPaymentStored):
    __version__ = 1

    _sid_field = 'id'
    _payment_suuid_field = 'payment_uuid'
    _order_id_field = 'order_id'
    _json_data_field = 'json_data'
    _is_delayed_payment_field = 'is_delayed_payment'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def create(self):
        logging.info('PayProGlobalPaymentDB create method')
        insert_sql = '''
                        INSERT INTO public.ppg_payment (
                            payment_uuid,
                            order_id,
                            json_data
                        )
                        VALUES (?, ?, ?)
                        RETURNING id;
                     '''
        insert_params = (
            self._payment_suuid,
            self._order_id,
            self._json_data,
        )
        logging.debug('Create PayProGlobalPaymentDB SQL : %s' % insert_sql)

        try:
            logging.debug('Call database service')
            self._sid = self._storage_service.create(sql=insert_sql, data=insert_params, is_return=True)[0].get(self._sid_field)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PPG_PAYMENT_CREATE_ERROR_DB.message
            error_code = BillingError.PPG_PAYMENT_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PPG_PAYMENT_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise PPGPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('PayProGlobalPaymentDB created.')

        return self._sid

    def update_by_order_id(self):
        logging.info('PayProGlobalPayment update method')

        update_sql = '''
                    UPDATE 
                      public.ppg_payment 
                    SET
                        id = ?,
                        payment_uuid = ?,
                        json_data = ?
                    WHERE 
                        order_id = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._sid,
            self._payment_suuid,
            self._json_data,
            self._order_id,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('PayProGlobalPayment updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PPG_PAYMENT_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PPG_PAYMENT_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = BillingError.PPG_PAYMENT_UPDATE_ERROR_DB.code
            raise PPGPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)

    def find_by_payment_suuid(self):
        logging.info('PayProGlobalPayment find_by_payment_suuid method')
        select_sql = '''
                    SELECT 
                          ppgp.id AS id,
                          ppgp.payment_uuid AS payment_uuid,
                          ppgp.order_id AS order_id,
                          ppgp.json_data AS json_data,
                          to_json(ppgp.created_date) AS created_date
                      FROM public.ppg_payment AS ppgp
                      WHERE ppgp.payment_uuid = ?
        '''

        logging.debug(f"select SQL: {select_sql}")
        params = (self._payment_suuid,)

        try:
            logging.debug('Call database service')
            ppg_payment_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTUUID_ERROR_DB.message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTUUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PPG_PAYMENT_FIND_BY_PAYMENTUUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise PPGPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(ppg_payment_list_db) == 1:
            ppg_payment_db = ppg_payment_list_db[0]
        elif len(ppg_payment_list_db) == 0:
            error_message = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTUUID_ERROR.message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTUUID_ERROR.code
            developer_message = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTUUID_ERROR.developer_message
            raise PPGPaymentNotFoundException(error=error_message, error_code=error_code,
                                              developer_message=developer_message)
        else:
            error_message = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTUUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % BillingError.PPG_PAYMENT_FIND_BY_PAYMENTUUID_ERROR.developer_message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTUUID_ERROR.code
            raise PPGPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__mappayproglobalpaymentdb_to_payproglobalpayment(ppg_payment_db)

    def find_by_order_id(self):
        logging.info('PayProGlobalPayment find_by_order_id method')
        select_sql = '''
                    SELECT 
                          ppgp.id AS id,
                          ppgp.payment_uuid AS payment_uuid,
                          ppgp.order_id AS order_id,
                          ppgp.json_data AS json_data,
                          to_json(ppgp.created_date) AS created_date
                      FROM public.ppg_payment AS ppgp
                      WHERE ppgp.order_id = ?
        '''

        logging.debug(f"Select SQL: {select_sql}")
        params = (self._order_id,)

        try:
            logging.debug('Call database service')
            ppg_payment_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR_DB.message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise PPGPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(ppg_payment_list_db) == 1:
            ppg_payment_db = ppg_payment_list_db[0]
        elif len(ppg_payment_list_db) == 0:
            error_message = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.code
            developer_message = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.developer_message
            raise PPGPaymentNotFoundException(error=error_message, error_code=error_code,
                                              developer_message=developer_message)
        else:
            error_message = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.developer_message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.code
            raise PPGPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__mappayproglobalpaymentdb_to_payproglobalpayment(ppg_payment_db)

    def __mappayproglobalpaymentdb_to_payproglobalpayment(self, payproglobalpayment_db):
        return PayProGlobalPayment(
            sid=payproglobalpayment_db[self._sid_field],
            payment_suuid=payproglobalpayment_db[self._payment_suuid_field],
            order_id=payproglobalpayment_db[self._order_id_field],
            json_data=payproglobalpayment_db[self._json_data_field],
            created_date=payproglobalpayment_db[self._created_date_field],
        )
