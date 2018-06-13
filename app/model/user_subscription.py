import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class UserSubscription(object):
    __version__ = 1

    _suuid = None
    _user_uuid = None
    _subscription_id = None
    _expire_date = None
    _order_uuid = None
    _modify_date = None
    _modify_reason = None
    _created_date = None

    def __init__(self, suuid: str = None, user_uuid: str = None, subscription_id: int = None, expire_date: datetime = None,
                 order_uuid: str = None, modify_date: datetime = None, modify_reason: str = None,
                 created_date: datetime = None):
        self._suuid = suuid
        self._user_uuid = user_uuid
        self._subscription_id = subscription_id
        self._expire_date = expire_date
        self._order_uuid = order_uuid
        self._modify_date = modify_date
        self._modify_reason = modify_reason
        self._created_date = created_date

    def to_dict(self):
        return {
            'uuid': str(self._suuid),
            'user_uuid': str(self._user_uuid),
            'subscription_id': self._subscription_id,
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
            'subscription_id': self._subscription_id,
            'expire_date': self._expire_date,
            'order_uuid': str(self._order_uuid),
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'created_date': self._created_date,
        }


class UserSubscriptionStored(StoredObject, UserSubscription):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, user_uuid: str = None, subscription_id: int = None,
                 expire_date: datetime = None, order_uuid: str = None, modify_date: datetime = None,
                 modify_reason: str = None, created_date: datetime = None, limit: int = None, offset: int = None,
                 **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        UserSubscription.__init__(self, suuid=suuid, user_uuid=user_uuid, subscription_id=subscription_id, expire_date=expire_date,
                                  modify_date=modify_date, modify_reason=modify_reason, order_uuid=order_uuid,
                                  created_date=created_date)


class UserSubscriptionDB(UserSubscriptionStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _user_uuid_field = 'user_uuid'
    _subscription_id_field = 'subscription_id'
    _expire_date_field = 'expire_date'
    _order_uuid_field = 'order_uuid'
    _modify_date_field = 'modify_date'
    _modify_reason_field = 'modify_reason'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find_by_uuid(self):
        logging.info('UserSubscriptionDB find_by_user_uuid_id method')
        select_sql = '''
                    SELECT 
                        us.uuid AS uuid,
                        us.user_uuid AS user_uuid,
                        us.subscription_id AS subscription_id,
                        to_json(us.expire_date) AS expire_date,
                        us.order_uuid AS order_uuid,
                        us.modify_reason AS modify_reason,
                        to_json(us.modify_date) AS modify_date,
                        to_json(us.created_date) AS created_date
                    FROM public.user_subscription us 
                    WHERE us.uuid = ?
        '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._suuid,)
        try:
            logging.debug('Call database service')
            user_subscription_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR_DB.message
            error_code = BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise UserSubscriptionException(error=error_message, error_code=error_code,
                                            developer_message=developer_message)

        if len(user_subscription_list_db) == 1:
            user_subscription_db = user_subscription_list_db[0]
        elif len(user_subscription_list_db) == 0:
            error_message = BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR.message
            error_code = BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR.code
            developer_message = BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR.developer_message
            raise UserSubscriptionNotFoundException(error=error_message, error_code=error_code,
                                                    developer_message=developer_message)
        else:
            error_message = BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % \
                                BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR.developer_message
            error_code = BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR.code
            raise UserSubscriptionException(error=error_message, error_code=error_code,
                                            developer_message=developer_message)

        return self.__map_user_subscriptiondb_to_user_subscription(user_subscription_db=user_subscription_db)

    def find_by_user_uuid(self):
        logging.info('UserSubscriptionDB find_by_user_uuid_id method')
        select_sql = '''
                    SELECT 
                        us.uuid AS uuid,
                        us.user_uuid AS user_uuid,
                        us.subscription_id AS subscription_id,
                        to_json(us.expire_date) AS expire_date,
                        us.order_uuid AS order_uuid,
                        us.modify_reason AS modify_reason,
                        to_json(us.modify_date) AS modify_date,
                        to_json(us.created_date) AS created_date
                    FROM public.user_subscription us 
                    WHERE us.user_uuid = ?
        '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._user_uuid,)
        try:
            logging.debug('Call database service')
            user_subscription_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.USER_SUBSCRIPTION_FIND_BY_USER_UUID_ERROR_DB.message
            error_code = BillingError.USER_SUBSCRIPTION_FIND_BY_USER_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.USER_SUBSCRIPTION_FIND_BY_USER_UUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise UserSubscriptionException(error=error_message, error_code=error_code,
                                            developer_message=developer_message)

        user_subscription_list = []
        for user_subscription_db in user_subscription_list_db:
            user_subscription = self.__map_user_subscriptiondb_to_user_subscription(user_subscription_db=user_subscription_db)
            user_subscription_list.append(user_subscription)

        return user_subscription_list

    def create(self):
        logging.info('UserSubscriptionDB create method')
        insert_sql = '''
                      INSERT INTO public.user_subscription
                        (user_uuid, subscription_id , expire_date, order_uuid)
                      VALUES 
                        (?, ?, ?, ?, ?, ?, ?)
                      RETURNING uuid
                     '''
        insert_params = (
            self._user_uuid,
            self._subscription_id,
            self._expire_date,
            self._order_uuid,
        )
        logging.debug('Create UserSubscriptionDB SQL : %s' % insert_sql)

        try:
            logging.debug('Call database service')
            self._suuid = self._storage_service.create(sql=insert_sql, data=insert_params)
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
        logging.debug('UserSubscriptionDB created.')

        return self._suuid

    def update(self):
        logging.info('UserSubscriptionDB update method')

        update_sql = '''
                    UPDATE public.user_subscription
                    SET
                        user_uuid = ?,
                        subscription_id = ?,
                        expire_date = ?,
                        order_uuid = ?,
                        modify_date = ?,
                        modify_reason = ?,
                    WHERE 
                        suuid = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._user_uuid,
            self._subscription_id,
            self._expire_date,
            self._order_uuid,
            self._modify_date,
            self._modify_reason,
            self._uuid,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('User Subscription updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.USER_SUBSCRIPTION_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.USER_SUBSCRIPTION_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = BillingError.USER_SUBSCRIPTION_UPDATE_ERROR_DB.code
            raise UserSubscriptionException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_user_subscriptiondb_to_user_subscription(self, user_subscription_db):
        return UserSubscription(
            suuid=user_subscription_db[self._suuid_field],
            user_uuid=user_subscription_db[self._user_uuid_field],
            subscription_id=user_subscription_db[self._subscription_id_field],
            expire_date=user_subscription_db[self._expire_date_field],
            order_uuid=user_subscription_db[self._order_uuid_field],
            modify_date=user_subscription_db[self._modify_date_field],
            modify_reason=user_subscription_db[self._modify_reason_field],
            created_date=user_subscription_db[self._created_date_field],
        )
