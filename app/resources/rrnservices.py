import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import RRNServiceException, BillingError
from app.model.service import RRNServiceDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(0, '../rest_api_library')
from api import ResourceAPI, APIResourceURL
from response import APIResponseStatus, APIResponse
from response import make_api_response, make_error_request_response


class RRNServicesAPI(ResourceAPI):
    __version__ = 1

    logger = logging.getLogger(__name__)

    __endpoint_name__ = __qualname__
    __api_url__ = 'services'

    _config = None

    Subscriptions_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, RRNServicesAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def put(self) -> Response:
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self) -> Response:
        super(RRNServicesAPI, self).get(req=request)

        service_db = RRNServiceDB(storage_service=self.__db_storage_service,
                                  limit=self.pagination.limit, offset=self.pagination.offset)

        try:
            service_list = service_db.find()
            service_list_dict = [service_list[i].to_api_dict() for i in range(0, len(service_list))]
        except RRNServiceException as e:
            self.logger.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                    data=service_list_dict, limit=self.pagination.limit,
                                    offset=self.pagination.offset)

        resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

        return resp
