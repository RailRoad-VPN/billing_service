import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class UserSubscription(object):
    __version__ = 1

    _user_uuid = None
    _subscription_id = None
    _expire_date = None
    _payment_id = None
    _created_date = None

    def __init__(self, user_uuid: str = None, subscription_id: int = None, expire_date: datetime = None,
                 payment_id: int = None, created_date: datetime = None):
        self._user_uuid = user_uuid
        self._subscription_id = subscription_id
        self._expire_date = expire_date
        self._payment_id = payment_id
        self._created_date = created_date

    def to_dict(self):
        return {
            'user_uuid': self._user_uuid,
            'subscription_id': self._subscription_id,
            'expire_date': self._expire_date,
            'payment_id': self._payment_id,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'user_uuid': str(self._user_uuid),
            'subscription_id': self._subscription_id,
            'expire_date': self._expire_date,
            'payment_id': self._payment_id,
            'created_date': self._created_date,
        }


class UserSubscriptionStored(StoredObject, UserSubscription):
    __version__ = 1

    def __init__(self, storage_service: StorageService, user_uuid: str = None, subscription_id: int = None,
                 expire_date: datetime = None, payment_id: int = None, created_date: datetime = None,
                 limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        UserSubscription.__init__(self, user_uuid=user_uuid, subscription_id=subscription_id, expire_date=expire_date,
                                  payment_id=payment_id, created_date=created_date)


class UserSubscriptionDB(UserSubscriptionStored):
    __version__ = 1

    _user_uuid_field = 'user_uuid'
    _subscription_id_field = 'subscription_id'
    _expire_date_field = 'expire_date'
    _payment_id_field = 'payment_id'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find_by_user_uuid(self):
        logging.info('UserSubscriptionDB find_by_user_uuid_id method')
        select_sql = '''
                    SELECT 
                      us.user_uuid AS user_uuid,
                      us.subscription_id AS subscription_id,
                      to_json(us.expire_date) AS expire_date,
                      us.payment_id AS payment_id,
                      to_json(us.created_date) AS created_date
                    FROM user_subscription us 
                    WHERE us.user_uuid = ?
        '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._user_uuid,)
        try:
            logging.debug('Call database service')
            user_subscription_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR_DB.message
            error_code = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise UserSubscriptionException(error=error_message, error_code=error_code,
                                            developer_message=developer_message)

        if len(user_subscription_list_db) == 1:
            user_subscription_db = user_subscription_list_db[0]
        elif len(user_subscription_list_db) == 0:
            error_message = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR.message
            error_code = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR.code
            developer_message = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR.developer_message
            raise UserSubscriptionNotFoundException(error=error_message, error_code=error_code,
                                                    developer_message=developer_message)
        else:
            error_message = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % \
                                BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR.developer_message
            error_code = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR.code
            raise UserSubscriptionException(error=error_message, error_code=error_code,
                                            developer_message=developer_message)

        return self.__mapuser_subscriptiondb_to_user_subscription(user_subscription_db=user_subscription_db)

    def __mapuser_subscriptiondb_to_user_subscription(self, user_subscription_db):
        return UserSubscription(
            user_uuid=user_subscription_db[self._user_uuid_field],
            subscription_id=user_subscription_db[self._subscription_id_field],
            expire_date=user_subscription_db[self._expire_date_field],
            payment_id=user_subscription_db[self._payment_id_field],
            created_date=user_subscription_db[self._created_date_field],
        )
