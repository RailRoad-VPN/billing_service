import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import UserRRNServiceException, BillingError, UserRRNServiceNotFoundException
from app.model.user_service import UserRRNServiceDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(0, '../rest_api_library')
from api import ResourceAPI, APIResourceURL
from utils import check_uuid
from response import APIResponseStatus, APIResponse, make_api_response, make_error_request_response, \
    check_required_api_fields


class UserRRNServicesAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = __qualname__
    __api_url__ = 'users/<string:user_uuid>/services'

    _config = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, UserRRNServicesAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST', ]),
            APIResourceURL(base_url=url, resource_name='<string:user_service_uuid>', methods=['GET', 'PUT', ]),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self, user_uuid: str) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.REQUEST_NO_JSON)

        is_valid = check_uuid(suuid=user_uuid)
        if not is_valid:
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=BillingError.BAD_IDENTITY_ERROR)

        user_uuid = request_json.get(UserRRNServiceDB._user_uuid_field, None)
        service_id = request_json.get(UserRRNServiceDB._service_id_field, None)
        status_id = request_json.get(UserRRNServiceDB._status_id_field, None)
        expire_date = request_json.get(UserRRNServiceDB._expire_date_field, None)
        order_uuid = request_json.get(UserRRNServiceDB._order_uuid_field, None)
        is_trial = request_json.get(UserRRNServiceDB._is_trial_field, None)

        try:
            req_fields = {
                'user_uuid': user_uuid,
                'status_id': status_id,
                'expire_date': expire_date,
                'service_id': service_id,
                'order_uuid': order_uuid,
                'is_trial': is_trial,
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

        user_service_db = UserRRNServiceDB(storage_service=self.__db_storage_service, user_uuid=user_uuid,
                                           status_id=status_id, service_id=service_id, is_trial=is_trial,
                                           expire_date=expire_date, order_uuid=order_uuid)

        try:
            user_service_uuid = user_service_db.create()
        except UserRRNServiceException as e:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        error_code=e.error_code, error=e.error, developer_message=e.developer_message)
            return make_api_response(data=response_data, http_code=response_data.code)

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.CREATED)
        resp = make_api_response(data=response_data, http_code=response_data.code)

        api_url = self.__api_url__.replace('<string:user_uuid>', user_uuid)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], api_url, user_service_uuid)
        return resp

    def put(self, user_uuid: str, user_service_uuid: str) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.REQUEST_NO_JSON)

        us_uuid = request_json.get('uuid', None)

        is_valid_a = check_uuid(suuid=user_service_uuid)
        is_valid_b = check_uuid(suuid=us_uuid)
        is_valid_c = check_uuid(suuid=user_uuid)
        if not is_valid_a or not is_valid_b or not is_valid_c or (user_service_uuid != us_uuid):
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=BillingError.BAD_IDENTITY_ERROR)

        user_uuid = request_json.get(UserRRNServiceDB._user_uuid_field, None)
        service_id = request_json.get(UserRRNServiceDB._service_id_field, None)
        status_id = request_json.get(UserRRNServiceDB._status_id_field, None)
        expire_date = request_json.get(UserRRNServiceDB._expire_date_field, None)
        order_uuid = request_json.get(UserRRNServiceDB._order_uuid_field, None)
        is_trial = request_json.get(UserRRNServiceDB._is_trial_field, None)
        modify_reason = request_json.get(UserRRNServiceDB._modify_reason_field, None)

        req_fields = {
            'user_uuid': user_uuid,
            'service_id': service_id,
            'status_id': status_id,
            'expire_date': expire_date,
            'order_uuid': order_uuid,
            'is_trial': is_trial,
            'modify_reason': modify_reason,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        user_service_db = UserRRNServiceDB(storage_service=self.__db_storage_service, suuid=us_uuid,
                                           user_uuid=user_uuid, service_id=service_id, is_trial=is_trial,
                                           expire_date=expire_date, order_uuid=order_uuid,
                                           modify_reason=modify_reason, status_id=status_id)
        try:
            user_service_db.find_by_uuid()
        except UserRRNServiceNotFoundException as e:
            # user service does not exist
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=BillingError.USER_SUBSCRIPTION_NOT_FOUND_ERROR)

        try:
            user_service_db.update()
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK)
            return make_api_response(data=response_data, http_code=response_data.code)
        except UserRRNServiceException as e:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        error_code=e.error_code, error=e.error, developer_message=e.developer_message)
            return make_api_response(data=response_data, http_code=response_data.code)

    def get(self, user_uuid: str, user_service_uuid: str = None) -> Response:
        super(UserRRNServicesAPI, self).get(req=request)

        is_valid = check_uuid(suuid=user_uuid)
        if not is_valid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                               err=BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR)

        user_service_db = UserRRNServiceDB(storage_service=self.__db_storage_service,
                                           suuid=user_service_uuid,
                                           user_uuid=user_uuid, limit=self.pagination.limit,
                                           offset=self.pagination.offset)
        if user_service_uuid is not None:
            # get specific user service
            is_valid = check_uuid(suuid=user_service_uuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                                   err=BillingError.USER_SUBSCRIPTION_FIND_BY_UUID_ERROR)

            try:
                user_service = user_service_db.find_by_uuid()

                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user_service.to_api_dict(), limit=self.pagination.limit,
                                            offset=self.pagination.offset)
                return make_api_response(data=response_data, http_code=HTTPStatus.OK)
            except UserRRNServiceException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except UserRRNServiceNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
        else:
            # get all user services
            try:
                user_service_list = user_service_db.find_by_user_uuid()
                user_service_dict = [user_service_list[i].to_api_dict() for i in
                                     range(0, len(user_service_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user_service_dict, limit=self.pagination.limit,
                                            offset=self.pagination.offset)
                return make_api_response(data=response_data, http_code=HTTPStatus.OK)
            except UserRRNServiceException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except UserRRNServiceNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
