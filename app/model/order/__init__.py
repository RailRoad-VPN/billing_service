import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import BillingError, OrderNotFoundException, OrderException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class Order(object):
    __version__ = 1

    _suuid = None
    _code = None
    _status_id = None
    _payment_uuid = None
    _modify_date = None
    _modify_reason = None
    _created_date = None

    def __init__(self, suuid: str = None, code: int = None, status_id: int = None, payment_uuid: str = None,
                 modify_date: datetime = None, modify_reason: str = None, created_date: datetime = None):
        self._suuid = suuid
        self._code = code
        self._status_id = status_id
        self._payment_uuid = payment_uuid
        self._modify_date = modify_date
        self._modify_reason = modify_reason
        self._created_date = created_date

    def to_dict(self):
        return {
            'uuid': str(self._suuid),
            'code': self._code,
            'status_id': self._status_id,
            'payment_uuid': str(self._payment_uuid),
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'uuid': str(self._suuid),
            'code': self._code,
            'status_id': self._status_id,
            'payment_uuid': str(self._payment_uuid) if self._payment_uuid else '',
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'created_date': self._created_date,
        }


class OrderStored(StoredObject, Order):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, code: int = None, status_id: int = None,
                 payment_uuid: str = None, created_date: datetime = None, modify_date: datetime = None,
                 modify_reason: str = None, limit: int = None, offset: int = None,
                 **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        Order.__init__(self, suuid=suuid, code=code, status_id=status_id, payment_uuid=payment_uuid,
                       modify_date=modify_date, modify_reason=modify_reason, created_date=created_date)


class OrderDB(OrderStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _code_field = 'code'
    _status_id_field = 'status_id'
    _payment_uuid_field = 'payment_uuid'
    _modify_date_field = 'modify_date'
    _modify_reason_field = 'modify_reason'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('OrderDB find method')
        select_sql = '''
                        SELECT
                            o.uuid AS uuid,
                            o.code AS code,
                            o.status_id AS status_id,
                            o.payment_uuid AS payment_uuid,
                            o.modify_reason AS modify_reason,
                            to_json(o.modify_date) AS modify_date,
                            to_json(o.created_date) AS created_date
                        FROM public.order o
                      '''
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            order_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.ORDER_FIND_ERROR_DB.message
            error_code = BillingError.ORDER_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                BillingError.ORDER_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise OrderException(error=error_message, error_code=error_code, developer_message=developer_message)
        order_list = []

        for order_db in order_list_db:
            order = self.__map_orderdb_to_order(order_db)
            order_list.append(order)

        return order_list

    def find_by_code(self):
        logging.info('OrderDB find_by_code method')
        select_sql = '''
                    SELECT
                        o.uuid AS uuid,
                        o.code AS code,
                        o.status_id AS status_id,
                        o.payment_uuid AS payment_uuid,
                        o.modify_reason AS modify_reason,
                        to_json(o.modify_date) AS modify_date,
                        to_json(o.created_date) AS created_date
                    FROM public.order o
                    WHERE o.code = ?
        '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (
            self._code,
        )
        try:
            logging.debug('Call database service')
            order_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.ORDER_FIND_BY_CODE_ERROR_DB.message
            error_code = BillingError.ORDER_FIND_BY_CODE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.ORDER_FIND_BY_CODE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise OrderException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(order_list_db) == 1:
            order_db = order_list_db[0]
        elif len(order_list_db) == 0:
            error_message = BillingError.ORDER_FIND_BY_CODE_ERROR.message
            error_code = BillingError.ORDER_FIND_BY_CODE_ERROR.code
            developer_message = BillingError.ORDER_FIND_BY_CODE_ERROR.developer_message
            raise OrderNotFoundException(error=error_message, error_code=error_code,
                                         developer_message=developer_message)
        else:
            error_message = BillingError.ORDER_FIND_BY_CODE_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % BillingError.ORDER_FIND_BY_CODE_ERROR.developer_message
            error_code = BillingError.ORDER_FIND_BY_CODE_ERROR.code
            raise OrderException(message=error_message, code=error_code, developer_message=developer_message)

        return self.__map_orderdb_to_order(order_db=order_db)

    def find_by_suuid(self):
        logging.info('OrderDB find_by_uuid method')
        select_sql = '''
                    SELECT
                        o.uuid AS uuid,
                        o.code AS code,
                        o.status_id AS status_id,
                        o.payment_uuid AS payment_uuid,
                        o.modify_reason AS modify_reason,
                        to_json(o.modify_date) AS modify_date,
                        to_json(o.created_date) AS created_date
                    FROM public.order o
                    WHERE o.uuid = ?
        '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (
            self._suuid,
        )
        try:
            logging.debug('Call database service')
            order_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.ORDER_FIND_BY_UUID_ERROR_DB.message
            error_code = BillingError.ORDER_FIND_BY_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.ORDER_FIND_BY_UUID_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise OrderException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(order_list_db) == 1:
            order_db = order_list_db[0]
        elif len(order_list_db) == 0:
            error_message = BillingError.ORDER_FIND_BY_UUID_ERROR.message
            error_code = BillingError.ORDER_FIND_BY_UUID_ERROR.code
            developer_message = BillingError.ORDER_FIND_BY_UUID_ERROR.developer_message
            raise OrderNotFoundException(error=error_message, error_code=error_code,
                                         developer_message=developer_message)
        else:
            error_message = BillingError.ORDER_FIND_BY_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % BillingError.ORDER_FIND_BY_UUID_ERROR.developer_message
            error_code = BillingError.ORDER_FIND_BY_UUID_ERROR.code
            raise OrderException(message=error_message, code=error_code, developer_message=developer_message)

        return self.__map_orderdb_to_order(order_db=order_db)

    def create(self):
        logging.info('OrderDB create method')
        insert_sql = '''
                      INSERT INTO public.order 
                        (code, status_id, payment_uuid) 
                      VALUES 
                        (?, ?, ?)
                      RETURNING uuid;
                     '''
        insert_params = (
            self._code,
            self._status_id,
            self._payment_uuid,
        )
        logging.debug('Create OrderDB SQL : %s' % insert_sql)

        try:
            logging.debug('Call database service')
            self._suuid = self._storage_service.create(sql=insert_sql, data=insert_params, is_return=True)[0][
                self._suuid_field]
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.ORDER_CREATE_ERROR_DB.message
            error_code = BillingError.ORDER_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.ORDER_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise OrderException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('OrderDB created.')

        return self._suuid

    def update(self):
        logging.info('OrderDB update method')

        update_sql = '''
                    UPDATE public.order 
                    SET
                        status_id = ?,
                        payment_uuid = ?,
                        modify_reason = ?
                    WHERE uuid = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._status_id,
            self._payment_uuid,
            self._modify_reason,
            self._suuid,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('OrderDB updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.ORDER_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.ORDER_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = BillingError.ORDER_UPDATE_ERROR_DB.code
            raise OrderException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_orderdb_to_order(self, order_db):
        return Order(
            suuid=order_db[self._suuid_field],
            code=order_db[self._code_field],
            status_id=order_db[self._status_id_field],
            payment_uuid=order_db[self._payment_uuid_field],
            modify_date=order_db[self._modify_date_field],
            modify_reason=order_db[self._modify_reason_field],
            created_date=order_db[self._created_date_field],
        )
