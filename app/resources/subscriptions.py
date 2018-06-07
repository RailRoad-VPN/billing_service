import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import SubscriptionException, BillingError
from app.model.subscription import SubscriptionDB
from app.model.subscription.feature import FeatureDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(0, '../rest_api_library')
from api import ResourceAPI
from response import APIResponseStatus, APIResponse
from utils import make_api_response
from rest import APIResourceURL


class SubscriptionsAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'SubscriptionsAPI'
    __api_url__ = 'subscriptions'

    _config = None

    Subscriptions_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, SubscriptionsAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        resp = make_api_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def put(self) -> Response:
        resp = make_api_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self) -> Response:
        super(SubscriptionsAPI, self).get(req=request)

        lang_code = request.headers.get('Accept-Language', None)

        if lang_code is None:
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=HTTPStatus.BAD_REQUEST,
                                        error=BillingError.BAD_ACCEPT_LANGUAGE_HEADER.message,
                                        developer_message=BillingError.BAD_ACCEPT_LANGUAGE_HEADER.description,
                                        error_code=BillingError.BAD_ACCEPT_LANGUAGE_HEADER.code)

            return make_api_response(data=response_data, http_code=HTTPStatus.BAD_REQUEST)

        subscription_db = SubscriptionDB(storage_service=self.__db_storage_service, lang_code=lang_code,
                                         limit=self.pagination.limit, offset=self.pagination.offset)

        try:
            subscription_list = subscription_db.find()
            subscription_list_dict = [subscription_list[i].to_api_dict() for i in range(0, len(subscription_list))]
        except SubscriptionException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        try:
            for subscription in subscription_list_dict:
                feature_db = FeatureDB(storage_service=self.__db_storage_service,
                                       subscription_id=subscription[SubscriptionDB._sid_field], lang_code=lang_code,
                                       limit=self.pagination.limit, offset=self.pagination.offset)
                feature_list = feature_db.find_by_subscription_id()
                subscription['features'] = [feature_list[i].to_api_dict() for i in range(0, len(feature_list))]
        except SubscriptionException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                    data=subscription_list_dict, limit=self.pagination.limit,
                                    offset=self.pagination.offset)

        resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

        return resp
