import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import BillingError, OrderPaymentException, OrderPaymentNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class OrderPayment(object):
    __version__ = 1

    _payment_uuid = None
    _order_uuid = None
    _created_date = None
    _type_id = None

    def __init__(self, order_uuid: str = None, payment_uuid: str = None, type_id: int = None,
                 created_date: datetime = None):
        self._payment_uuid = payment_uuid
        self._order_uuid = order_uuid
        self._type_id = type_id
        self._created_date = created_date

    def to_dict(self):
        return {
            'payment_uuid': self._payment_uuid,
            'order_uuid': self._order_uuid,
            'type_id': self._type_id,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'payment_uuid': str(self._payment_uuid),
            'order_uuid': str(self._order_uuid),
            'type_id': self._type_id,
            'created_date': self._created_date,
        }


class OrderPaymentStored(StoredObject, OrderPayment):
    __version__ = 1

    def __init__(self, storage_service: StorageService, payment_uuid: str = None, order_uuid: str = None,
                 type_id: str = None, created_date: datetime = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        OrderPayment.__init__(self, order_uuid=order_uuid, payment_uuid=payment_uuid, type_id=type_id,
                              created_date=created_date)


class OrderPaymentDB(OrderPaymentStored):
    __version__ = 1

    _payment_uuid_field = 'payment_uuid'
    _order_uuid_field = 'order_uuid'
    _type_id_field = 'type_id'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('OrderPaymentDB find method')
        select_sql = '''
                    SELECT op.payment_uuid AS payment_uuid,
                           op.order_uuid AS order_uuid,
                           op.type_id AS type_id,
                           to_json(op.created_date) AS created_date
                    FROM public.order_payment op
                      '''
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        logging.debug(f"select SQL: {select_sql}")

        try:
            logging.debug('Call database service')
            order_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.ORDERPAYMENT_FIND_ERROR_DB.message
            error_code = BillingError.ORDERPAYMENT_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.ORDERPAYMENT_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise OrderPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)
        order_list = []

        for order_db in order_list_db:
            order = self.__map_orderdb_to_order(order_db)
            order_list.append(order)

        return order_list

    def find_by_payment(self):
        logging.info('OrderPaymentDB find_by_order method')
        select_sql = '''
                    SELECT op.payment_uuid AS payment_uuid,
                           op.order_uuid AS order_uuid,
                           op.type_id AS type_id,
                           to_json(op.created_date) AS created_date
                    FROM public.order_payment op
                    WHERE op.payment_uuid = ?
        '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (
            self._payment_uuid,
        )
        try:
            logging.debug('Call database service')
            order_payment_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.ORDERPAYMENT_FIND_BY_PAYMENT_ERROR_DB.message
            error_code = BillingError.ORDERPAYMENT_FIND_BY_PAYMENT_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.ORDERPAYMENT_FIND_BY_PAYMENT_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise OrderPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(order_payment_list_db) == 1:
            order_payment_db = order_payment_list_db[0]
        elif len(order_payment_list_db) == 0:
            error_message = BillingError.ORDERPAYMENT_FIND_BY_PAYMENT_ERROR.message
            error_code = BillingError.ORDERPAYMENT_FIND_BY_PAYMENT_ERROR.code
            developer_message = BillingError.ORDERPAYMENT_FIND_BY_PAYMENT_ERROR.developer_message
            raise OrderPaymentNotFoundException(error=error_message, error_code=error_code,
                                                developer_message=developer_message)
        else:
            error_message = BillingError.ORDERPAYMENT_FIND_BY_PAYMENT_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % BillingError.ORDERPAYMENT_FIND_BY_PAYMENT_ERROR.developer_message
            error_code = BillingError.ORDERPAYMENT_FIND_BY_PAYMENT_ERROR.code
            raise OrderPaymentException(message=error_message, code=error_code, developer_message=developer_message)

        return self.__map_orderdb_to_order(order_payment_db=order_payment_db)

    def find_by_order(self):
        logging.info('OrderPaymentDB find_by_order method')
        select_sql = '''
                    SELECT op.payment_uuid AS payment_uuid,
                           op.order_uuid AS order_uuid,
                           op.type_id AS type_id,
                           to_json(op.created_date) AS created_date
                    FROM public.order_payment op
                    WHERE op.order_uuid = ?
        '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (
            self._order_uuid,
        )
        try:
            logging.debug('Call database service')
            order_payment_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.ORDERPAYMENT_FIND_BY_ORDER_ERROR_DB.message
            error_code = BillingError.ORDERPAYMENT_FIND_BY_ORDER_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.ORDERPAYMENT_FIND_BY_ORDER_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise OrderPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)

        order_payment_list = []
        for order_payment_db in order_payment_list_db:
            order_payment = self.__map_orderdb_to_order(order_payment_db=order_payment_db)
            order_payment_list.append(order_payment)

        return order_payment_list

    def create(self):
        logging.info('OrderPaymentDB create method')
        insert_sql = '''
                      INSERT INTO public.order_payment 
                        (order_uuid, type_id) 
                      VALUES 
                        (?, ?)
                      RETURNING payment_uuid
                     '''
        insert_params = (
            self._order_uuid,
            self._type_id,
        )
        logging.debug(f"create OrderPaymentDB SQL: {insert_sql}")

        try:
            logging.debug('Call database service')
            self._payment_uuid = self._storage_service.create(sql=insert_sql, data=insert_params, is_return=True)[0][self._payment_uuid_field]
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.ORDERPAYMENT_CREATE_ERROR_DB.message
            error_code = BillingError.ORDERPAYMENT_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.ORDERPAYMENT_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise OrderPaymentException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('OrderPaymentDB created.')

        return self._payment_uuid

    def __map_orderdb_to_order(self, order_payment_db):
        return OrderPayment(
            payment_uuid=order_payment_db[self._payment_uuid_field],
            order_uuid=order_payment_db[self._order_uuid_field],
            type_id=order_payment_db[self._type_id_field],
            created_date=order_payment_db[self._created_date_field],
        )
