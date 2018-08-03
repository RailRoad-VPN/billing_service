import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import BillingError, PaymentException, OrderPaymentException, \
    OrderPaymentNotFoundException, PPGPaymentException, PPGPaymentNotFoundException
from app.model import PaymentType
from app.model.order.payments import OrderPaymentDB
from app.model.order.payments.payproglobal import PayProGlobalPaymentDB
from utils import check_uuid

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(0, '../rest_api_library')
from api import ResourceAPI
from response import make_api_response, make_error_request_response, APIResponse, APIResponseStatus, \
    check_required_api_fields
from rest import APIResourceURL

logger = logging.getLogger(__name__)


class OrderPaymentsAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'OrderPaymentsAPI'
    __api_url__ = 'orders/<string:order_uuid>/payments'

    _config = None

    Payments_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = f"{base_url}/{OrderPaymentsAPI.__api_url__}"
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:suuid>', methods=['GET']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self, order_uuid: str) -> Response:
        logger.debug(f"create payment for order_uuid: {order_uuid}")

        logger.debug("check order_uuid")
        is_valid = check_uuid(order_uuid)
        if not is_valid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.ORDER_IDENTIFIER_ERROR)

        request_json = request.json

        logger.debug("check is request has json")
        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.REQUEST_NO_JSON)

        logger.debug("get type_id from request_json")
        type_id = request_json.get(OrderPaymentDB._type_id_field, None)
        logger.debug(f"type_id: {type_id}")

        req_fields = {
            'type_id': type_id,
        }

        logger.debug(f"check required fields: {req_fields}")
        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        logger.debug("create order_payment_db instance")
        order_payment_db = OrderPaymentDB(storage_service=self.__db_storage_service, order_uuid=order_uuid,
                                          type_id=type_id)

        try:
            logger.debug("create order_payment in database")
            payment_uuid = order_payment_db.create()
        except PaymentException as e:
            logger.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        logger.debug("check payment type in PPG and PPG_TEST")
        if type_id in [PaymentType.PAYPROGLOBAL.sid, PaymentType.PAYPROGLOBAL_TEST.sid]:
            order_id = request_json.get(PayProGlobalPaymentDB._order_id_field, None)
            json_data = request_json.get(PayProGlobalPaymentDB._json_data_field, None)

            req_fields = {
                'order_id': order_id,
                'json_data': json_data
            }

            logger.debug(f"check required fields: {req_fields}")
            error_fields = check_required_api_fields(req_fields)
            if len(error_fields) > 0:
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                            errors=error_fields)
                resp = make_api_response(data=response_data, http_code=response_data.code)
                return resp

            logger.debug("create ppg_payment_db instance")
            ppg_payment_db = PayProGlobalPaymentDB(storage_service=self.__db_storage_service,
                                                   payment_suuid=payment_uuid, order_id=order_id, json_data=json_data)

            try:
                logger.debug("create ppg payment in database")
                ppg_payment_db.create()
            except PPGPaymentException as e:
                logger.error(e)
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
        resp = make_api_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self, order_uuid: str, suuid: str = None) -> Response:
        super(OrderPaymentsAPI, self).get(req=request)

        logger.debug(f"OrderPaymentsAPI -> GET method with parameters: order_uuid: {order_uuid}, suuid: {suuid}")

        if suuid is not None:
            logger.debug(f"check order_payment uuid")
            is_valid = check_uuid(suuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.ORDER_IDENTIFIER_ERROR)

            logger.debug("create order_payment_db instance")
            order_payment_db = OrderPaymentDB(storage_service=self.__db_storage_service, order_uuid=order_uuid,
                                              payment_uuid=suuid)
            try:
                logger.debug("find order_payment in database")
                order_payment = order_payment_db.find_by_payment()
                payment = self._get_payment(order_payment_dict=order_payment.to_dict())
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
                                        data=payment.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

            return resp
        else:
            logger.debug(f"get all order payments")

            logger.debug("create order_payment_db instance")
            order_payment_db = OrderPaymentDB(storage_service=self.__db_storage_service, order_uuid=order_uuid)

            try:
                logger.debug(f"find all order_payments")
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

            logger.debug("find additional information for every order_payment")

            payment_list = []
            order_payment_list_dict = [order_payment_list[i].to_api_dict() for i in range(0, len(order_payment_list))]
            for order_payment_dict in order_payment_list_dict:
                payment = self._get_payment(order_payment_dict=order_payment_dict)
                payment_list.append(payment)

            payment_list_dict = [payment_list[i].to_api_dict() for i in range(0, len(payment_list))]
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                        data=payment_list_dict)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

            return resp

    def _get_payment(self, order_payment_dict: dict):
        logger.debug(f"process order_payment: {order_payment_dict}")
        payment_uuid = order_payment_dict[OrderPaymentDB._payment_uuid_field]
        payment_type_id = order_payment_dict[OrderPaymentDB._type_id_field]

        payment = None
        if payment_type_id in [PaymentType.PAYPROGLOBAL.sid, PaymentType.PAYPROGLOBAL_TEST.sid]:
            logger.debug("create ppg_payment_db instance")
            ppg_payment_db = PayProGlobalPaymentDB(storage_service=self.__db_storage_service,
                                                   payment_suuid=payment_uuid)
            try:
                payment = ppg_payment_db.find_by_payment_suuid()
            except PPGPaymentNotFoundException as e:
                pass
                # TODO fix it
            except PPGPaymentException as e:
                pass
                # TODO fix it
        return payment