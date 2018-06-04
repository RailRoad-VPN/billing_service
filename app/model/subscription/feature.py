import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class Feature(object):
    __version__ = 1

    _sid = None
    _subscription_id = None
    _name = None
    _tooltip = None
    _enabled = None
    _lang_code = None
    _modify_date = None
    _modify_reason = None
    _created_date = None

    def __init__(self, sid: int = None, subscription_id: int = None, name: str = None, tooltip: str = None,
                 enabled: bool = None, lang_code: str = None, modify_date: datetime = None, modify_reason: str = None,
                 created_date: datetime = None):
        self._sid = sid
        self._subscription_id = subscription_id
        self._name = name
        self._tooltip = tooltip
        self._enabled = enabled
        self._lang_code = lang_code
        self._modify_date = modify_date
        self._modify_reason = modify_reason
        self._created_date = created_date

    def to_dict(self):
        return {
            'id': self._sid,
            'subscription_id': self._subscription_id,
            'name': self._name,
            'tooltip': self._tooltip,
            'enabled': self._enabled,
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'id': self._sid,
            'subscription_id': self._subscription_id,
            'name': self._name,
            'tooltip': self._tooltip,
            'enabled': self._enabled,
        }


class FeatureStored(StoredObject, Feature):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, subscription_id: int = None, name: str = None,
                 tooltip: str = None, enabled: bool = None, lang_code: str = None, modify_date: datetime = None,
                 modify_reason: str = None, created_date: datetime = None, limit: int = None, offset: int = None,
                 **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        Feature.__init__(self, sid=sid, subscription_id=subscription_id, name=name, tooltip=tooltip,
                         enabled=enabled, lang_code=lang_code, modify_date=modify_date, modify_reason=modify_reason,
                         created_date=created_date)


class FeatureDB(FeatureStored):
    __version__ = 1

    _sid_field = 'id'
    _subscription_id_field = 'subscription_id'
    _name_field = 'name'
    _tooltip_field = 'tooltip'
    _enabled_field = 'enabled'
    _modify_date_field = 'modify_date'
    _modify_reason_field = 'modify_reason'
    _lang_code_field = 'lang_code'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find_by_subscription_id(self):
        logging.info('FeatureDB find method')
        select_sql = '''
                    SELECT
                      sf.id              AS id,
                      sf.subscription_id AS subscription_id,
                      sft.name           AS name,
                      sft.tooltip        AS tooltip,
                      sf.enabled         AS enabled,
                      sft.lang_code      AS lang_code,
                      sf.modify_date     AS modify_date,
                      sf.modify_reason   AS modify_reason,
                      sf.created_date    AS created_date
                    FROM public.subscription_feature sf
                      JOIN subscription_feature_translation sft ON sf.id = sft.subscription_feature_id
                    WHERE sf.subscription_id = ? AND sft.lang_code = ?
        '''
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._subscription_id, self._lang_code)
        try:
            logging.debug('Call database service')
            feature_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.FEATURE_FIND_ERROR_DB.phrase
            error_code = BillingError.FEATURE_FIND_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.FEATURE_FIND_ERROR_DB.description, e.pgcode, e.pgerror)
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)

        feature_list = []
        for feature_db in feature_list_db:
            feature = self.__mapfeaturedb_to_feature(feature_db=feature_db)
            feature_list.append(feature)

        return feature_list

    def __mapfeaturedb_to_feature(self, feature_db):
        return Feature(
            sid=feature_db[self._sid_field],
            subscription_id=feature_db[self._subscription_id_field],
            name=feature_db[self._name_field],
            tooltip=feature_db[self._tooltip_field],
            enabled=feature_db[self._enabled_field],
            lang_code=feature_db[self._lang_code_field],
            modify_date=feature_db[self._modify_date_field],
            modify_reason=feature_db[self._modify_reason_field],
            created_date=feature_db[self._created_date_field],
        )
