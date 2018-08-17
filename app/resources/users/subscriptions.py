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
from utils import check_uuid
from response import APIResponseStatus, APIResponse, make_api_response, make_error_request_response, \
    check_required_api_fields
from rest import APIResourceURL


class UsersSubscriptionsAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = __qualname__
    __api_url__ = 'users/<string:user_uuid>/subscriptions'

    _config = None

    UserSubscriptions_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, UsersSubscriptionsAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST', ]),
            APIResourceURL(base_url=url, resource_name='<string:user_subscription_uuid>', methods=['GET', 'PUT', ]),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self, user_uuid: str) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.REQUEST_NO_JSON)

        is_valid = check_uuid(suuid=user_uuid)
        if not is_valid:
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=BillingError.BAD_IDENTITY_ERROR)

        user_uuid = request_json.get(UserSubscriptionDB._user_uuid_field, None)
        subscription_id = request_json.get(UserSubscriptionDB._subscription_id_field, None)
        status_id = request_json.get(UserSubscriptionDB._status_id_field, None)
        expire_date = request_json.get(UserSubscriptionDB._expire_date_field, None)
        order_uuid = request_json.get(UserSubscriptionDB._order_uuid_field, None)

        try:
            req_fields = {
                'user_uuid': user_uuid,
                'status_id': status_id,
                'subscription_id': subscription_id,
                'order_uuid': order_uuid,
            }
        except TypeError:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        user_subscription_db = UserSubscriptionDB(storage_service=self.__db_storage_service, user_uuid=user_uuid,
                                                  status_id=status_id, subscription_id=subscription_id,
                                                  expire_date=expire_date, order_uuid=order_uuid)

        try:
            user_subscription_uuid = user_subscription_db.create()
        except UserSubscriptionException as e:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        error_code=e.error_code, error=e.error, developer_message=e.developer_message)
            return make_api_response(data=response_data, http_code=response_data.code)

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.CREATED)
        resp = make_api_response(data=response_data, http_code=response_data.code)

        api_url = self.__api_url__.replace('<string:user_uuid>', user_uuid)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], api_url, user_subscription_uuid)
        return resp

    def put(self, user_uuid: str, user_subscription_uuid: str) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.REQUEST_NO_JSON)

        us_uuid = request_json.get('uuid', None)

        is_valid_a = check_uuid(suuid=user_subscription_uuid)
        is_valid_b = check_uuid(suuid=us_uuid)
        is_valid_c = check_uuid(suuid=user_uuid)
        if not is_valid_a or not is_valid_b or not is_valid_c or (user_subscription_uuid != us_uuid):
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=BillingError.BAD_IDENTITY_ERROR)

        user_uuid = request_json.get(UserSubscriptionDB._user_uuid_field, None)
        subscription_id = request_json.get(UserSubscriptionDB._subscription_id_field, None)
        status_id = request_json.get(UserSubscriptionDB._status_id_field, None)
        expire_date = request_json.get(UserSubscriptionDB._expire_date_field, None)
        order_uuid = request_json.get(UserSubscriptionDB._order_uuid_field, None)
        modify_reason = request_json.get(UserSubscriptionDB._modify_reason_field, None)

        req_fields = {
            'user_uuid': user_uuid,
            'subscription_id': subscription_id,
            'status_id': status_id,
            'expire_date': expire_date,
            'order_uuid': order_uuid,
            'modify_reason': modify_reason,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        user_subscription_db = UserSubscriptionDB(storage_service=self.__db_storage_service, suuid=us_uuid,
                                                  user_uuid=user_uuid, subscription_id=subscription_id,
                                                  expire_date=expire_date, order_uuid=order_uuid,
                                                  modify_reason=modify_reason, status_id=status_id)
        try:
            user_subscription_db.find_by_uuid()
        except UserSubscriptionNotFoundException as e:
            # user subscription does not exist
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=BillingError.USER_SUBSCRIPTION_NOT_FOUND_ERROR)

        try:
            user_subscription_db.update()
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK)
            return make_api_response(data=response_data, http_code=response_data.code)
        except UserSubscriptionException as e:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        error_code=e.error_code, error=e.error, developer_message=e.developer_message)
            return make_api_response(data=response_data, http_code=response_data.code)

    def get(self, user_uuid: str, user_subscription_uuid: str = None) -> Response:
        super(UsersSubscriptionsAPI, self).get(req=request)

        is_valid = check_uuid(suuid=user_uuid)
        if not is_valid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                               err=BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR)

        user_subscription_db = UserSubscriptionDB(storage_service=self.__db_storage_service,
                                                  suuid=user_subscription_uuid,
                                                  user_uuid=user_uuid, limit=self.pagination.limit,
                                                  offset=self.pagination.offset)
        if user_subscription_uuid is not None:
            # get specific user subscription
            is_valid = check_uuid(suuid=user_subscription_uuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                                   err=BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR)

            try:
                user_subscription = user_subscription_db.find_by_uuid()

                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user_subscription.to_api_dict(), limit=self.pagination.limit,
                                            offset=self.pagination.offset)
                return make_api_response(data=response_data, http_code=HTTPStatus.OK)
            except UserSubscriptionException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except UserSubscriptionNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
        else:
            # get all user subscriptions
            try:
                user_subscription_list = user_subscription_db.find_by_user_uuid()
                user_subscription_dict = [user_subscription_list[i].to_api_dict() for i in
                                          range(0, len(user_subscription_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user_subscription_dict, limit=self.pagination.limit,
                                            offset=self.pagination.offset)
                return make_api_response(data=response_data, http_code=HTTPStatus.OK)
            except UserSubscriptionException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except UserSubscriptionNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
