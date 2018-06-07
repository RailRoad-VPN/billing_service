import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import UserSubscriptionException, BillingError, UserSubscriptionNotFoundException
from app.model.user_subscription import UserSubscriptionDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(0, '../rest_api_library')
from api import ResourceAPI
from response import APIResponseStatus, APIResponse
from utils import make_api_response, check_uuid
from rest import APIResourceURL


class UserSubscriptionsAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'UserSubscriptionsAPI'
    __api_url__ = 'user_subscriptions'

    _config = None

    UserSubscriptions_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, UserSubscriptionsAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='<string:user_uuid>', methods=['GET', 'POST', 'PUT']),
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

    def get(self, user_uuid: str) -> Response:
        super(UserSubscriptionsAPI, self).get(req=request)

        if user_uuid is not None:
            is_valid = check_uuid(suuid=user_uuid)
            if not is_valid:
                error = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR.message
                error_code = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR.code
                developer_message = BillingError.USER_SUBSCRIPTION_FINDBYUUID_ERROR.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp

        user_subscription_db = UserSubscriptionDB(storage_service=self.__db_storage_service, user_uuid=user_uuid,
                                                  limit=self.pagination.limit, offset=self.pagination.offset)

        try:
            user_subscription = user_subscription_db.find_by_user_uuid()

            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=user_subscription.to_api_dict(), limit=self.pagination.limit,
                                        offset=self.pagination.offset)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
            return resp
        except UserSubscriptionException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)
        except UserSubscriptionNotFoundException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.NOT_FOUND
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)
