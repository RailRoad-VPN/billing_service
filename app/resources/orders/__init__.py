import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import BillingError, OrderException, OrderNotFoundException
from app.model.order import OrderDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(0, '../rest_api_library')
from api import ResourceAPI
from utils import check_uuid
from response import make_api_response, make_error_request_response, check_required_api_fields
from rest import APIResourceURL
from response import APIResponse, APIResponseStatus

logger = logging.getLogger(__name__)


class OrdersAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'OrdersAPI'
    __api_url__ = 'orders'

    _config = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, OrdersAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:suuid>', methods=['PUT']),
            APIResourceURL(base_url=url, resource_name='code/<int:code>', methods=['GET']),
            APIResourceURL(base_url=url, resource_name='uuid/<string:suuid>', methods=['GET']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.REQUEST_NO_JSON)

        code = request_json.get(OrderDB._code_field, None)
        status_id = request_json.get(OrderDB._status_id_field, None)

        req_fields = {
            'status_id': status_id,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        order_db = OrderDB(storage_service=self.__db_storage_service, code=code, status_id=status_id)

        try:
            order_db.find_by_code()
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.ORDER_CREATE_CODE_EXIST_ERROR)
        except OrderNotFoundException:
            try:
                suuid = order_db.create()
            except OrderException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.CREATED)
        resp = make_api_response(data=response_data, http_code=HTTPStatus.CREATED)
        resp.headers['Location'] = f"{self._config['API_BASE_URI']}/{self.__api_url__}/uuid/{suuid}"
        return resp

    def put(self, suuid: str) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.REQUEST_NO_JSON)

        order_uuid = request_json.get(OrderDB._suuid_field, None)

        is_valid_suuid = check_uuid(suuid)
        is_valid_order_uuid = check_uuid(order_uuid)
        if not is_valid_suuid or not is_valid_order_uuid or suuid != order_uuid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.ORDER_IDENTIFIER_ERROR)

        code = request_json.get(OrderDB._code_field, None)
        status_id = request_json.get(OrderDB._status_id_field)
        modify_reason = request_json.get(OrderDB._modify_reason_field)

        req_fields = {
            'code': code,
            'status_id': status_id,
            'modify_reason': modify_reason,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        order_db = OrderDB(storage_service=self.__db_storage_service, suuid=suuid, code=code, status_id=status_id,
                           modify_reason=modify_reason)

        try:
            order_db.find_by_code()
        except OrderNotFoundException:
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=BillingError.ORDER_UPDATE_NOT_EXIST_ERROR)

        try:
            order_db.update()
        except OrderException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK)
        resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        return resp

    def get(self, suuid: str = None, code: int = None) -> Response:
        super(OrdersAPI, self).get(req=request)

        order_db = OrderDB(storage_service=self.__db_storage_service, suuid=suuid, code=code,
                           limit=self.pagination.limit, offset=self.pagination.offset)

        if suuid is not None:
            is_valid = check_uuid(suuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.ORDER_IDENTIFIER_ERROR)

            try:
                order = order_db.find_by_suuid()
            except OrderNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except OrderException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                        data=order.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        elif code is not None:
            try:
                order = order_db.find_by_code()
            except OrderNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except OrderException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                        data=order.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        else:
            # list of all servers
            try:
                order_list = order_db.find()
            except OrderNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except OrderException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

            orders_dict = [order_list[i].to_api_dict() for i in range(0, len(order_list))]
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK, data=orders_dict,
                                        limit=self.pagination.limit, offset=self.pagination.offset)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

        return resp
