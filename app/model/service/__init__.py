import datetime
import logging

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class RRNService(object):
    __version__ = 1

    _sid = None
    _service_name = None
    _description = None
    _price = None
    _old_price = None
    _billed_period = None
    _modify_date = None
    _modify_reason = None
    _created_date = None
    _is_free = None
    _is_trial = None
    _trial_period_days = None
    _type_id = None
    _type_name = None

    def __init__(self, sid: int = None, service_name: str = None, description: str = None, price: int = None,
                 old_price: int = None, billed_period: int = None, modify_date: datetime = None, is_trial: bool = None,
                 trial_period_days: int = None, modify_reason: str = None, created_date: datetime = None,
                 type_id: int = None, type_name: str = None, is_free: bool = None):
        self._sid = sid
        self._service_name = service_name
        self._description = description
        self._price = price
        self._old_price = old_price
        self._billed_period = billed_period
        self._modify_date = modify_date
        self._modify_reason = modify_reason
        self._created_date = created_date
        self._is_free = is_free
        self._is_trial = is_trial
        self._trial_period_days = trial_period_days
        self._type_id = type_id
        self._type_name = type_name

    def to_dict(self):
        return {
            'id': self._sid,
            'service_name': self._service_name,
            'description': self._description,
            'price': self._price,
            'old_price': self._old_price,
            'billed_period': self._billed_period,
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'created_date': self._created_date,
            'is_free': self._is_free,
            'is_trial': self._is_trial,
            'trial_period_days': self._trial_period_days,
            'type': {
                'id': self._type_id,
                'name': self._type_name,
            }
        }

    def to_api_dict(self):
        return {
            'id': self._sid,
            'service_name': self._service_name,
            'description': self._description,
            'price': self._price,
            'old_price': self._old_price,
            'billed_period': self._billed_period,
            'is_free': self._is_free,
            'is_trial': self._is_trial,
            'trial_period_days': self._trial_period_days,
            'type': {
                'id': self._type_id,
                'name': self._type_name,
            }
        }


class RRNServiceStored(StoredObject, RRNService):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, price: int = None,
                 old_price: int = None, billed_period: int = None, modify_date: datetime = None,
                 is_trial: bool = None, trial_period_days: int = None, is_free: bool = None,
                 modify_reason: str = None, created_date: datetime = None, service_name: str = None,
                 description: str = None, type_id: int = None, type_name: str = None,
                 limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        RRNService.__init__(self, sid=sid, price=price, old_price=old_price, type_id=type_id, type_name=type_name,
                            billed_period=billed_period, modify_date=modify_date, is_trial=is_trial, is_free=is_free,
                            trial_period_days=trial_period_days, modify_reason=modify_reason, created_date=created_date,
                            service_name=service_name, description=description)


class RRNServiceDB(RRNServiceStored):
    __version__ = 1

    _sid_field = 'id'
    _service_name_field = 'name'
    _description_field = 'description'
    _price_field = 'price'
    _old_price_field = 'old_price'
    _billed_period_field = 'billed_period'
    _modify_date_field = 'modify_date'
    _modify_reason_field = 'modify_reason'
    _created_date_field = 'created_date'
    _is_free_field = 'is_free'
    _is_trial_field = 'is_trial'
    _trial_period_days_field = 'trial_period_days'
    _type_id_field = 'type_id'
    _type_name_field = 'type_name'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        self.logger.info('RRNServiceDB find method')
        select_sql = '''
                    SELECT
                      s.id                      AS id,
                      s.name                    AS name,
                      s.description             AS description,
                      s.price                   AS price,
                      s.old_price               AS old_price,
                      s.is_free                 AS is_free,
                      s.is_trial                AS is_trial,
                      s.trial_period_days       AS trial_period_days,
                      s.billed_period           AS billed_period,
                      s.modify_date             AS modify_date,
                      s.modify_reason           AS modify_reason,
                      s.created_date            AS created_date,
                      s.type_id                 AS type_id,
                      st.name                   AS type_name
                    FROM public.service s
                      JOIN public.service_type st ON s.type_id = st.id
                    ORDER BY s.id ASC
        '''
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")
        try:
            self.logger.debug('Call database service')
            service_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.SERVICE_FIND_ERROR_DB.message
            error_code = BillingError.SERVICE_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    BillingError.SERVICE_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise RRNServiceException(error=error_message, error_code=error_code, developer_message=developer_message)

        service_list = []
        for service_db in service_list_db:
            subscription = self._map_servicedb_to_service(service_db=service_db)
            service_list.append(subscription)

        return service_list

    def find_by_id(self):
        self.logger.info('RRNServiceDB find_by_id method')
        select_sql = '''
                    SELECT
                      s.id                      AS id,
                      s.name                    AS name,
                      s.description             AS description,
                      s.price                   AS price,
                      s.old_price               AS old_price,
                      s.billed_period           AS billed_period,
                      s.is_free                 AS is_free,
                      s.is_trial                AS is_trial,
                      s.trial_period_days       AS trial_period_days,
                      s.modify_date             AS modify_date,
                      s.modify_reason           AS modify_reason,
                      s.created_date            AS created_date,
                      s.type_id                 AS type_id,
                      st.name                   AS type_name
                    FROM public.service s
                      JOIN public.service_type st ON s.type_id = st.id
                    WHERE s.id = ?
        '''

        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")
        select_params = (self._sid,)
        try:
            self.logger.debug('Call database service')
            service_list_db = self._storage_service.get(sql=select_sql, data=select_params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.SERVICE_FIND_BY_ID_ERROR_DB.message
            error_code = BillingError.SERVICE_FIND_BY_ID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    BillingError.SERVICE_FIND_BY_ID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise RRNServiceException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(service_list_db) == 1:
            service_db = service_list_db[0]
        elif len(service_list_db) == 0:
            error_message = BillingError.SERVICE_FIND_BY_ID_ERROR.message
            error_code = BillingError.SERVICE_FIND_BY_ID_ERROR.code
            developer_message = BillingError.SERVICE_FIND_BY_ID_ERROR.developer_message
            raise RRNServiceNotFoundException(error=error_message, error_code=error_code,
                                              developer_message=developer_message)
        else:
            error_message = BillingError.SERVICE_FIND_BY_ID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % BillingError.SERVICE_FIND_BY_ID_ERROR.developer_message
            error_code = BillingError.SERVICE_FIND_BY_ID_ERROR.code
            raise RRNServiceException(message=error_message, code=error_code, developer_message=developer_message)

        return self._map_servicedb_to_service(service_db=service_db)

    def _map_servicedb_to_service(self, service_db):
        return RRNService(
            sid=service_db[self._sid_field],
            service_name=service_db[self._service_name_field],
            description=service_db[self._description_field],
            price=service_db[self._price_field],
            old_price=service_db[self._old_price_field],
            billed_period=service_db[self._billed_period_field],
            is_free=service_db[self._is_free_field],
            is_trial=service_db[self._is_trial_field],
            trial_period_days=service_db[self._trial_period_days_field],
            modify_date=service_db[self._modify_date_field],
            modify_reason=service_db[self._modify_reason_field],
            created_date=service_db[self._created_date_field],
            type_id=service_db[self._type_id_field],
            type_name=service_db[self._type_name_field],
        )
