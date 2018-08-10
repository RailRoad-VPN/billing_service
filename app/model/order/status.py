import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import BillingError, BillingException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class OrderStatus(object):
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


class OrderStatusStored(StoredObject, OrderStatus):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, name: int = None, limit: int = None,
                 offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        OrderStatus.__init__(self, sid=sid, name=name)


class OrderStatusDB(OrderStatusStored):
    __version__ = 1

    _sid_field = 'id'
    _name_field = 'name'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('OrderStatus find method')
        select_sql = '''
                      SELECT 
                        id,
                        name
                      FROM public.order_status
                      '''
        logging.debug(f"Select SQL: {select_sql}")

        try:
            logging.debug('Call database service')
            order_status_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.ORDERSTATUS_FIND_ERROR_DB.message
            error_code = BillingError.ORDERSTATUS_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    BillingError.ORDERSTATUS_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)
        order_status_list = []

        for order_status_db in order_status_list_db:
            order_status = self.__map_order_statusdb_to_order_status(order_status_db)
            order_status_list.append(order_status)

        if len(order_status_list) == 0:
            logging.warning('Empty OrderStatus list of method find. Very strange behaviour.')

        return order_status_list

    def __map_order_statusdb_to_order_status(self, order_status_db):
        return OrderStatus(
            sid=order_status_db[self._sid_field],
            name=order_status_db[self._name_field],
        )
