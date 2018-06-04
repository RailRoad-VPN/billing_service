import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class Subscription(object):
    __version__ = 1

    _sid = None
    _price_per_month = None
    _old_price_per_month = None
    _billed_period_in_months = None
    _billed_period_in_years = None
    _is_best = None
    _modify_date = None
    _modify_reason = None
    _created_date = None
    _name = None
    _description = None
    _bill_freq = None
    _lang_code = None

    def __init__(self, sid: int = None, price_per_month: int = None, old_price_per_month: int = None,
                 billed_period_in_months: int = None, billed_period_in_years: int = None, is_best: bool = None,
                 modify_date: datetime = None, modify_reason: str = None, created_date: datetime = None,
                 name: str = None, description: str = None, bill_freq: str = None, lang_code: str = None):
        self._sid = sid
        self._price_per_month = price_per_month
        self._old_price_per_month = old_price_per_month
        self._billed_period_in_months = billed_period_in_months
        self._billed_period_in_years = billed_period_in_years
        self._is_best = is_best
        self._modify_date = modify_date
        self._modify_reason = modify_reason
        self._created_date = created_date
        self._name = name
        self._description = description
        self._bill_freq = bill_freq
        self._lang_code = lang_code

    def to_dict(self):
        return {
            'id': self._sid,
            'price_per_month': self._price_per_month,
            'old_price_per_month': self._old_price_per_month,
            'billed_period_in_months': self._billed_period_in_months,
            'billed_period_in_years': self._billed_period_in_years,
            'is_best': self._is_best,
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'created_date': self._created_date,
            'name': self._name,
            'description': self._description,
            'bill_freq': self._bill_freq,
            'lang_code': self._lang_code,
        }

    def to_api_dict(self):
        return {
            'id': self._sid,
            'price_per_month': self._price_per_month,
            'old_price_per_month': self._old_price_per_month,
            'billed_period_in_months': self._billed_period_in_months,
            'billed_period_in_years': self._billed_period_in_years,
            'is_best': self._is_best,
            'name': self._name,
            'description': self._description,
            'bill_freq': self._bill_freq,
        }


class SubscriptionStored(StoredObject, Subscription):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, price_per_month: int = None,
                 old_price_per_month: int = None, billed_period_in_months: int = None,
                 billed_period_in_years: int = None, is_best: bool = None, modify_date: datetime = None,
                 modify_reason: str = None, created_date: datetime = None, name: str = None, description: str = None,
                 bill_freq: str = None, lang_code: str = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        Subscription.__init__(self, sid=sid, price_per_month=price_per_month, old_price_per_month=old_price_per_month,
                              billed_period_in_months=billed_period_in_months,
                              billed_period_in_years=billed_period_in_years, is_best=is_best, modify_date=modify_date,
                              modify_reason=modify_reason, created_date=created_date, name=name,
                              description=description, bill_freq=bill_freq, lang_code=lang_code)


class SubscriptionDB(SubscriptionStored):
    __version__ = 1

    _sid_field = 'id'
    _price_per_month_field = 'price_per_month'
    _old_price_per_month_field = 'old_price_per_month'
    _billed_period_in_months_field = 'billed_period_in_months'
    _billed_period_in_years_field = 'billed_period_in_years'
    _is_best_field = 'is_best'
    _modify_date_field = 'modify_date'
    _modify_reason_field = 'modify_reason'
    _created_date_field = 'created_date'
    _name_field = 'name'
    _description_field = 'description'
    _bill_freq_field = 'bill_freq'
    _lang_code_field = 'lang_code'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('SubscriptionDB find method')
        select_sql = '''
                    SELECT
                      s.id                      AS id,
                      s.price_per_month         AS price_per_month,
                      s.old_price_per_month     AS old_price_per_month,
                      s.billed_period_in_months AS billed_period_in_months,
                      s.billed_period_in_years  AS billed_period_in_years,
                      s.is_best                 AS is_best,
                      s.modify_date             AS modify_date,
                      s.modify_reason           AS modify_reason,
                      s.created_date            AS created_date,
                      st.name                   AS name,
                      st.description            AS description,
                      st.bill_freq              AS bill_freq,
                      st.lang_code              AS lang_code
                    FROM public.subscription s
                      JOIN public.subscription_translation st ON s.id = st.subscription_id
                    WHERE st.lang_code = ?
        '''
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        logging.debug('Select SQL: %s' % select_sql)
        select_params = (self._lang_code,)
        try:
            logging.debug('Call database service')
            subscription_list_db = self._storage_service.get(sql=select_sql, data=select_params)
        except DatabaseError as e:
            logging.error(e)
            error_message = BillingError.SUBSCRIPTION_FIND_ERROR_DB.phrase
            error_code = BillingError.SUBSCRIPTION_FIND_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.SUBSCRIPTION_FIND_ERROR_DB.description, e.pgcode, e.pgerror)
            raise SubscriptionException(error=error_message, error_code=error_code, developer_message=developer_message)

        subscription_list = []
        for subscription_db in subscription_list_db:
            subscription = self.__mapsubscriptiondb_to_subscription(subscription_db=subscription_db)
            subscription_list.append(subscription)

        return subscription_list

    def __mapsubscriptiondb_to_subscription(self, subscription_db):
        return Subscription(
            sid=subscription_db[self._sid_field],
            price_per_month=subscription_db[self._price_per_month_field],
            old_price_per_month=subscription_db[self._old_price_per_month_field],
            billed_period_in_months=subscription_db[self._billed_period_in_months_field],
            billed_period_in_years=subscription_db[self._billed_period_in_years_field],
            is_best=subscription_db[self._is_best_field],
            modify_date=subscription_db[self._modify_date_field],
            modify_reason=subscription_db[self._modify_reason_field],
            created_date=subscription_db[self._created_date_field],
            name=subscription_db[self._name_field],
            description=subscription_db[self._description_field],
            bill_freq=subscription_db[self._bill_freq_field],
            lang_code=subscription_db[self._lang_code_field],
        )
