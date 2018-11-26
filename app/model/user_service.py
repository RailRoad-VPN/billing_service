import datetime
import logging

from dateutil.relativedelta import relativedelta
from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class UserRRNService(object):
    __version__ = 1

    logger = logging.getLogger(__name__)

    _suuid = None
    _user_uuid = None
    _service_id = None
    _status_id = None
    _is_trial = None
    _expire_date = None
    _order_uuid = None
    _modify_date = None
    _modify_reason = None
    _created_date = None

    def __init__(self, suuid: str = None, user_uuid: str = None, service_id: int = None, status_id: int = None,
                 expire_date: datetime = None, order_uuid: str = None, modify_date: datetime = None,
                 is_trial: bool = None, modify_reason: str = None, created_date: datetime = None):
        self._suuid = suuid
        self._user_uuid = user_uuid
        self._service_id = service_id
        self._expire_date = expire_date
        self._status_id = status_id
        self._is_trial = is_trial
        self._order_uuid = order_uuid
        self._modify_date = modify_date
        self._modify_reason = modify_reason
        self._created_date = created_date

    def to_dict(self):
        return {
            'uuid': str(self._suuid),
            'user_uuid': str(self._user_uuid),
            'service_id': self._service_id,
            'status_id': self._status_id,
            'is_trial': self._is_trial,
            'expire_date': self._expire_date,
            'order_uuid': str(self._order_uuid),
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'uuid': str(self._suuid),
            'user_uuid': str(self._user_uuid),
            'service_id': self._service_id,
            'status_id': self._status_id,
            'is_trial': self._is_trial,
            'expire_date': self._expire_date,
            'order_uuid': str(self._order_uuid),
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'created_date': self._created_date,
        }


class UserRRNServiceStored(StoredObject, UserRRNService):
    __version__ = 1

    logger = logging.getLogger(__name__)

    def __init__(self, storage_service: StorageService, suuid: str = None, user_uuid: str = None, status_id: int = None,
                 service_id: int = None, expire_date: datetime = None, order_uuid: str = None, is_trial: bool = None,
                 modify_date: datetime = None, modify_reason: str = None, created_date: datetime = None,
                 limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        UserRRNService.__init__(self, suuid=suuid, user_uuid=user_uuid, service_id=service_id, is_trial=is_trial,
                                expire_date=expire_date, modify_date=modify_date, modify_reason=modify_reason,
                                order_uuid=order_uuid, created_date=created_date, status_id=status_id)


class UserRRNServiceDB(UserRRNServiceStored):
    __version__ = 1

    logger = logging.getLogger(__name__)

    _suuid_field = 'uuid'
    _user_uuid_field = 'user_uuid'
    _service_id_field = 'service_id'
    _status_id_field = 'status_id'
    _is_trial_field = 'is_trial'
    _expire_date_field = 'expire_date'
    _order_uuid_field = 'order_uuid'
    _modify_date_field = 'modify_date'
    _modify_reason_field = 'modify_reason'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find_by_uuid(self):
        self.logger.info('UserRRNServiceDB find_by_uuid method')
        select_sql = '''
                    SELECT 
                        us.uuid AS uuid,
                        us.user_uuid AS user_uuid,
                        us.service_id AS service_id,
                        us.status_id AS status_id,
                        us.is_trial AS is_trial,
                        to_json(us.expire_date) AS expire_date,
                        us.order_uuid AS order_uuid,
                        us.modify_reason AS modify_reason,
                        to_json(us.modify_date) AS modify_date,
                        to_json(us.created_date) AS created_date
                    FROM public.user_service us 
                    WHERE us.uuid = ?
        '''
        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")
        params = (self._suuid,)
        try:
            self.logger.debug('Call database service')
            user_service_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.USER_SERVICE_FIND_BY_UUID_ERROR_DB.message
            error_code = BillingError.USER_SERVICE_FIND_BY_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    BillingError.USER_SERVICE_FIND_BY_UUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise UserRRNServiceException(error=error_message, error_code=error_code,
                                          developer_message=developer_message)

        if len(user_service_list_db) == 1:
            user_service_db = user_service_list_db[0]
        elif len(user_service_list_db) == 0:
            error_message = BillingError.USER_SERVICE_FIND_BY_UUID_ERROR.message
            error_code = BillingError.USER_SERVICE_FIND_BY_UUID_ERROR.code
            developer_message = BillingError.USER_SERVICE_FIND_BY_UUID_ERROR.developer_message
            raise UserRRNServiceNotFoundException(error=error_message, error_code=error_code,
                                                  developer_message=developer_message)
        else:
            error_message = BillingError.USER_SERVICE_FIND_BY_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % \
                                BillingError.USER_SERVICE_FIND_BY_UUID_ERROR.developer_message
            error_code = BillingError.USER_SERVICE_FIND_BY_UUID_ERROR.code
            raise UserRRNServiceException(error=error_message, error_code=error_code,
                                          developer_message=developer_message)

        return self.from_db_to_obj(user_service_db=user_service_db)

    def find_by_user_uuid(self):
        self.logger.info('UserRRNServiceDB find_by_user_uuid method')
        select_sql = '''
                    SELECT 
                        us.uuid AS uuid,
                        us.user_uuid AS user_uuid,
                        us.service_id AS service_id,
                        us.status_id AS status_id,
                        us.is_trial AS is_trial,
                        to_json(us.expire_date) AS expire_date,
                        us.order_uuid AS order_uuid,
                        us.modify_reason AS modify_reason,
                        to_json(us.modify_date) AS modify_date,
                        to_json(us.created_date) AS created_date
                    FROM public.user_service us 
                    WHERE us.user_uuid = ?
        '''
        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")
        params = (self._user_uuid,)
        try:
            self.logger.debug('Call database service')
            user_service_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.USER_SERVICE_FIND_BY_USER_UUID_ERROR_DB.message
            error_code = BillingError.USER_SERVICE_FIND_BY_USER_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    BillingError.USER_SERVICE_FIND_BY_USER_UUID_ERROR_DB.developer_message,
                                    e.pgcode,
                                    e.pgerror)
            raise UserRRNServiceException(error=error_message, error_code=error_code,
                                          developer_message=developer_message)

        user_service_list = []
        for user_service_db in user_service_list_db:
            user_service = self.from_db_to_obj(user_service_db=user_service_db)
            user_service_list.append(user_service)

        return user_service_list

    def create(self):
        self.logger.info('UserRRNServiceDB create method')
        insert_sql = '''
                      INSERT INTO public.user_service
                        (user_uuid, expire_date, service_id, order_uuid, is_trial, status_id)
                      VALUES 
                        (?, ?, ?, ?, ?, ?)
                      RETURNING uuid
                     '''
        insert_params = (
            self._user_uuid,
            self._expire_date,
            self._service_id,
            self._order_uuid,
            self._is_trial,
            self._status_id,
        )
        self.logger.debug('Create UserRRNServiceDB SQL : %s' % insert_sql)

        try:
            self.logger.debug('Call database service')
            self._suuid = self._storage_service.create(sql=insert_sql, data=insert_params, is_return=True)[0][
                self._suuid_field]
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.USER_SERVICE_CREATE_ERROR_DB.message
            error_code = BillingError.USER_SERVICE_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    BillingError.USER_SERVICE_CREATE_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)

            raise UserRRNServiceException(error=error_message, error_code=error_code,
                                          developer_message=developer_message)
        self.logger.debug('UserRRNServiceDB created.')

        return self._suuid

    def update(self):
        self.logger.info('UserRRNServiceDB update method')

        update_sql = '''
                    UPDATE public.user_service
                    SET
                        user_uuid = ?,
                        service_id = ?,
                        status_id = ?,
                        is_trial = ?,
                        expire_date = ?,
                        order_uuid = ?,
                        modify_reason = ?
                    WHERE uuid = ?
                    '''

        self.logger.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._user_uuid,
            self._service_id,
            self._status_id,
            self._is_trial,
            self._expire_date,
            self._order_uuid,
            self._modify_reason,
            self._suuid,
        )

        try:
            self.logger.debug(f"{self.__class__}: Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            self.logger.debug('User Service updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.USER_SERVICE_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    BillingError.USER_SERVICE_UPDATE_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            error_code = BillingError.USER_SERVICE_UPDATE_ERROR_DB.code
            raise UserRRNServiceException(error=error_message, error_code=error_code,
                                          developer_message=developer_message)

    def from_db_to_obj(self, user_service_db):
        return UserRRNService(
            suuid=user_service_db[self._suuid_field],
            user_uuid=user_service_db[self._user_uuid_field],
            service_id=user_service_db[self._service_id_field],
            status_id=user_service_db[self._status_id_field],
            is_trial=user_service_db[self._is_trial_field],
            expire_date=user_service_db[self._expire_date_field],
            order_uuid=user_service_db[self._order_uuid_field],
            modify_date=user_service_db[self._modify_date_field],
            modify_reason=user_service_db[self._modify_reason_field],
            created_date=user_service_db[self._created_date_field],
        )
