import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import BillingError, PaymentException, OrderPaymentException, \
    OrderPaymentNotFoundException
from app.model.order.payments import OrderPaymentDB
from utils import check_uuid

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(0, '../rest_api_library')
from api import ResourceAPI, APIResourceURL
from response import make_api_response, make_error_request_response, APIResponse, APIResponseStatus, \
    check_required_api_fields


class OrdersPaymentsAPI(ResourceAPI):
    __version__ = 1

    logger = logging.getLogger(__name__)

    __endpoint_name__ = __qualname__
    __api_url__ = 'orders/<string:order_uuid>/payments'

    _config = None

    Payments_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = f"{base_url}/{OrdersPaymentsAPI.__api_url__}"
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:suuid>', methods=['GET']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self, order_uuid: str) -> Response:
        self.logger.debug(f"{self.__class__}: create payment for order_uuid: {order_uuid}")

        self.logger.debug(f"{self.__class__}: check order_uuid")
        is_valid = check_uuid(order_uuid)
        if not is_valid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.ORDER_IDENTIFIER_ERROR)

        request_json = request.json

        self.logger.debug(f"{self.__class__}: check is request has json")
        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.REQUEST_NO_JSON)

        self.logger.debug(f"{self.__class__}: get data from request_json")
        order_uuid = request_json.get(OrderPaymentDB._order_uuid_field, None)
        type_id = request_json.get(OrderPaymentDB._type_id_field, None)
        status_id = request_json.get(OrderPaymentDB._status_id_field, None)
        json_data = request_json.get(OrderPaymentDB._json_data_field, None)
        self.logger.debug(f"{self.__class__}: order_uuid={order_uuid}, type_id={type_id}, status_id={status_id}, json_data={json_data}")

        req_fields = {
            'order_uuid': order_uuid,
            'type_id': type_id,
            'status_id': status_id,
            'json_data': json_data,
        }

        self.logger.debug(f"{self.__class__}: check required fields: {req_fields}")
        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        self.logger.debug(f"{self.__class__}: create order_payment_db instance")
        order_payment_db = OrderPaymentDB(storage_service=self.__db_storage_service, order_uuid=order_uuid,
                                          status_id=status_id, type_id=type_id, json_data=json_data)

        try:
            self.logger.debug(f"{self.__class__}: create order_payment in database")
            payment_uuid = order_payment_db.create()
        except PaymentException as e:
            self.logger.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.CREATED)
        resp = make_api_response(data=response_data, http_code=HTTPStatus.CREATED)
        api_url = self.__api_url__.replace("<string:order_uuid>", order_uuid)
        resp.headers['Location'] = f"{self._config['API_BASE_URI']}/{api_url}/{payment_uuid}"
        return resp

    def put(self) -> Response:
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self, order_uuid: str, suuid: str = None) -> Response:
        super(OrdersPaymentsAPI, self).get(req=request)

        self.logger.debug(f"{self.__class__}: OrderPaymentsAPI -> GET method with parameters: order_uuid: {order_uuid}, suuid: {suuid}")

        if suuid is not None:
            self.logger.debug(f"{self.__class__}: check order_payment uuid")
            is_valid = check_uuid(suuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.ORDER_IDENTIFIER_ERROR)

            self.logger.debug(f"{self.__class__}: create order_payment_db instance")
            order_payment_db = OrderPaymentDB(storage_service=self.__db_storage_service, order_uuid=order_uuid,
                                              suuid=suuid)
            try:
                self.logger.debug(f"{self.__class__}: find order_payment in database")
                order_payment = order_payment_db.find_by_payment()
            except OrderPaymentNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except OrderPaymentException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                        data=order_payment.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

            return resp
        else:
            self.logger.debug(f"{self.__class__}: get all order payments")

            self.logger.debug(f"{self.__class__}: create order_payment_db instance")
            order_payment_db = OrderPaymentDB(storage_service=self.__db_storage_service, order_uuid=order_uuid)

            try:
                self.logger.debug(f"{self.__class__}: find all order_payments")
                order_payment_list = order_payment_db.find_by_order()
            except OrderPaymentException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

            order_payment_list_dict = [order_payment_list[i].to_api_dict() for i in range(0, len(order_payment_list))]
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                        data=order_payment_list_dict)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

            return resp
