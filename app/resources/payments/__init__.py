import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import BillingError, PaymentException, PaymentNotFoundException
from app.model import PaymentType
from app.model.payments import PaymentDB
from app.model.payments.payproglobal import PayProGlobalPaymentDB
from utils import check_uuid

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(0, '../rest_api_library')
from api import ResourceAPI
from response import make_api_response, make_error_request_response, APIResponse, APIResponseStatus, \
    check_required_api_fields
from rest import APIResourceURL

logger = logging.getLogger(__name__)


class PaymentsAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'PaymentsAPI'
    __api_url__ = 'payments'

    _config = None

    Payments_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = f"{base_url}/{PaymentsAPI.__api_url__}"
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['POST']),
            APIResourceURL(base_url=url, resource_name='<string:suuid>', methods=['GET']),
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

        type_id = request_json.get(PaymentDB._type_id_field, None)

        req_fields = {
            'type_id': type_id,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        payment_db = PaymentDB(storage_service=self.__db_storage_service, type_id=type_id)

        try:
            payment_uuid = payment_db.create()
        except PaymentException as e:
            logger.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        if type_id in [PaymentType.PAYPROGLOBAL.sid, PaymentType.PAYPROGLOBAL_TEST.sid]:
            order_id = request_json.get(PayProGlobalPaymentDB._order_id_field, None)
            json_data = request_json.get(PayProGlobalPaymentDB._json_data_field, None)

            ppg_payment_db = PayProGlobalPaymentDB(storage_service=self.__db_storage_service,
                                                   payment_suuid=payment_uuid, order_id=order_id, json_data=json_data)

            try:
                ppg_payment_db.create()
            except PaymentException as e:
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
        resp.headers['Location'] = f"{self._config['API_BASE_URI']}/{self.__api_url__}/{payment_uuid}"
        return resp

    def put(self) -> Response:
        resp = make_api_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self, suuid: str) -> Response:
        super(PaymentsAPI, self).get(req=request)

        payment_db = PaymentDB(storage_service=self.__db_storage_service, suuid=suuid, limit=self.pagination.limit,
                               offset=self.pagination.offset)

        is_valid = check_uuid(suuid)
        if not is_valid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=BillingError.ORDER_IDENTIFIER_ERROR)

        try:
            payment = payment_db.find_by_uuid()
        except PaymentNotFoundException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.NOT_FOUND
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)
        except PaymentException as e:
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
