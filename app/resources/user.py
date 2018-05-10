import datetime
import json
import logging
import uuid as uuidlib
from typing import List, Optional

from flask import Response, request, make_response
from psycopg2._psycopg import DatabaseError

from app.common import JSONDecimalEncoder
from app.common.exception import UserNotFoundException, UserException, AuthError
from app.common.storage import StorageService, DBStorageService
from app.resources import API


class User(object):
    __version__ = 1

    _uuid = None
    _email = None
    _created_date = None
    _password = None
    _account_non_expired = False
    _account_non_locked = False
    _credentials_non_expired = False
    _enabled = False

    def __init__(self, uuid: str, email: str, created_date: datetime, password: str,
                 account_non_expired: bool, account_non_locked: bool, credentials_non_expired: bool, enabled: bool):
        self._uuid = uuid
        self._email = email
        self._created_date = created_date
        self._password = password
        self._account_non_expired = account_non_expired
        self._account_non_locked = account_non_locked
        self._credentials_non_expired = credentials_non_expired
        self._enabled = enabled

    def to_dict(self):
        return {
            'uuid': self._uuid,
            'email': self._email,
            'created_date': self._created_date,
            'password': self._password,
            'account_non_expired': self._account_non_expired,
            'account_non_locked': self._account_non_locked,
            'credentials_non_expired': self._credentials_non_expired,
            'enabled': self._enabled,
        }


class UserStored(User):
    __version__ = 1

    _storage_service = None

    def __init__(self, storage_service: StorageService, **kwargs: dict) -> None:
        super().__init__(**kwargs)

        self._storage_service = storage_service


class UserDB(UserStored):
    __version__ = 1

    __uuid_field = 'uuid'
    __email_field = 'email'
    __created_date_field = 'created_date'
    __password_field = 'password'
    __account_non_expired_field = 'account_non_expired'
    __account_non_locked_field = 'account_non_locked'
    __credentials_non_expired_field = 'credentials_non_expired'
    __enabled_field = 'enabled'

    def __init__(self, **kwargs: dict) -> None:
        super().__init__(**kwargs)

    def create(self) -> str:
        self._uuid = uuidlib.uuid4()
        logging.info('Create object User with uuid: ' + str(self._uuid))
        create_user_sql = 'INSERT INTO public."user" (uuid, email, password, enabled, account_non_expired, ' \
                          'account_non_locked, credentials_non_expired) VALUES (?, ?, ?, ?, ?, ?, ?)'
        create_user_params = (
            self._uuid,
            self._email,
            self._password,
            self._enabled,
            self._account_non_expired,
            self._account_non_locked,
            self._credentials_non_expired
        )
        logging.debug('Create User SQL : %s' % create_user_sql)

        try:
            logging.debug('Call database service')
            self._storage_service.create(create_user_sql, create_user_params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            code = e.pgcode
            error_message = 'Internal system error'
            system_error_code = AuthError.USER_CREATE_ERROR_DB
            developer_message = 'DatabaseError: %s . Something wrong with database or SQL is broken.' % e.pgerror
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)
        logging.debug('User created.')

        return self._uuid

    def update(self):
        # TODO update user social network
        logging.info('Update User')

        update_sql = '''
                    UPDATE public."user" 
                    SET email = ?,
                      enabled = ?,
                      password = ?, 
                      account_non_expired = ?, 
                      account_non_locked = ?, 
                      credentials_non_expired = ?
                    WHERE 
                      uuid = ?;
        '''

        logging.debug('Update SQL: %s' % update_sql)

        params = (
            self._email, self._password, self._enabled, self._account_non_expired,
            self._account_non_locked, self._credentials_non_expired, self._uuid
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(update_sql, params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            code = e.pgcode
            error_message = 'Internal database error'
            developer_message = "DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (e.pgcode, e.pgerror)
            system_error_code = AuthError.USER_UPDATE_ERROR_DB
            data = {
                'code': code,
                'message': error_message,
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)

    def find_by_uuid(self) -> Optional[User]:
        logging.info('Find User by uuid')
        select_sql = 'SELECT * FROM public."user" WHERE uuid = ?'
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._uuid,)

        try:
            logging.debug('Call database service')
            user_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            code = e.pgcode
            error_message = 'Internal system error'
            system_error_code = AuthError.USER_FINDBYUUID_ERROR_DB
            developer_message = 'DatabaseError: %s . Something wrong with database or SQL is broken.' % e.pgerror
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)

        if len(user_list_db) == 1:
            user_db = user_list_db[0]
        elif len(user_list_db) == 0:
            error_message = "User not found"
            system_error_code = AuthError.USER_FINDBYUUID_ERROR
            data = {
                'system_error_code': system_error_code,
                'developer_message': None
            }
            raise UserNotFoundException(message=error_message, code=system_error_code, data=data)
        else:
            error_message = "User not found"
            developer_message = "Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database."
            system_error_code = AuthError.USER_FINDBYUUID_ERROR
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=system_error_code, data=data)

        return self.__map_userdb_to_user(user_db)

    def find_by_email(self) -> Optional[User]:
        logging.info('Find User by email')
        select_sql = 'SELECT * FROM public."user" WHERE email = ?'
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._email,)

        try:
            logging.debug('Call database service')
            user_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            code = e.pgcode
            error_message = 'Internal system error'
            system_error_code = AuthError.USER_FINDBYEMAIL_ERROR_DB
            developer_message = 'DatabaseError: %s . Something wrong with database or SQL is broken.' % e.pgerror
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)

        if len(user_list_db) == 1:
            user_db = user_list_db[0]
        elif len(user_list_db) == 0:
            error_message = "User not found"
            system_error_code = AuthError.USER_FINDBYEMAIL_ERROR
            data = {
                'system_error_code': system_error_code,
                'developer_message': None
            }
            raise UserNotFoundException(message=error_message, code=system_error_code, data=data)
        else:
            error_message = "User not found"
            developer_message = "Find by specified email return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database."
            system_error_code = AuthError.USER_FINDBYEMAIL_ERROR
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=system_error_code, data=data)

        return self.__map_userdb_to_user(user_db)

    def find_all(self) -> Optional[List[User]]:
        logging.info('Find all Users')
        select_sql = 'SELECT * FROM public."user"'
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            user_db_list = self._storage_service.get(select_sql)
        except DatabaseError as e:
            logging.error(e)
            code = e.pgcode
            error_message = 'Internal system error'
            system_error_code = AuthError.USER_FINDALL_ERROR_DB
            developer_message = 'DatabaseError: %s . Something wrong with database or SQL is broken.' % e.pgerror
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)
        user_list = []

        for user_db in user_db_list:
            user = self.__map_userdb_to_user(user_db)
            user_list.append(user)

        if len(user_list) == 0:
            logging.warning('Empty User list of method find_all. Very strange behaviour.')

        return user_list

    def __map_userdb_to_user(self, user_db):
        self._uuid = user_db[self.__uuid_field]
        return User(uuid=self._uuid,
                    email=user_db[self.__email_field],
                    account_non_expired=user_db[self.__account_non_expired_field],
                    account_non_locked=user_db[self.__account_non_locked_field],
                    credentials_non_expired=user_db[self.__credentials_non_expired_field],
                    created_date=user_db[self.__created_date_field],
                    password=user_db[self.__password_field],
                    enabled=user_db[self.__enabled_field])


class UserAPI(API):
    __version__ = 1

    __api_url__ = 'users'

    __uuid_field = 'uuid'
    __email_field = 'email'
    __password_field = 'password'
    __account_non_expired_field = 'account_non_expired'
    __account_non_locked_field = 'account_non_locked'
    __credentials_non_expired_field = 'credentials_non_expired'
    __enabled_field = 'enabled'

    __db_storage_service = None

    def __init__(self, db_storage_service: DBStorageService) -> None:
        super().__init__()
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        email = request_json[self.__email_field]
        password = request_json.get(self.__password_field, None)
        account_non_expired = request_json.get(self.__account_non_expired_field, True)
        account_non_locked = request_json.get(self.__account_non_locked_field, True)
        credentials_non_expired = request_json.get(self.__credentials_non_expired_field, True)
        enabled = request_json.get(self.__enabled_field, True)

        user_db = UserDB(storage_service=self.__db_storage_service, email=email,
                         password=password, account_non_expired=account_non_expired,
                         account_non_locked=account_non_locked, credentials_non_expired=credentials_non_expired,
                         enabled=enabled)

        try:
            uuid = user_db.create()
        except UserException as e:
            logging.error(e)
            code = e.code
            message = e.message
            data_err = e.data
            data = {
                'error': {
                    'code': code,
                    'message': message,
                    'data': data_err
                }
            }
            if code == AuthError.USER_CREATE_ERROR_DB:
                http_code = 400
            else:
                http_code = 500
            return make_response(json.dumps(data), http_code)

        resp = make_response("", 201)
        resp.headers['Location'] = '%s/%s/uuid/%s' % (cfg.API_BASE_URI, self.__api_url__, uuid)
        return resp

    def put(self, uuid: str = None) -> Response:
        request_json = request.json
        user_uuid = request_json[self.__uuid_field]
        if uuid != user_uuid:
            return make_response('', 404)

        try:
            uuidlib.UUID(user_uuid)
        except ValueError as e:
            message = 'User not found'
            developer_message = 'Bad uuid value.'
            system_error_code = AuthError.USER_FINDBYUUID_ERROR
            logging.error(e)
            data_err = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            data = {
                'error': {
                    'code': system_error_code,
                    'message': message,
                    'data': data_err
                }
            }
            resp = make_response(json.dumps(data), 404)
            return resp

        email = request_json[self.__email_field]
        password = request_json[self.__password_field]
        account_non_expired = request_json[self.__account_non_expired_field]
        account_non_locked = request_json[self.__account_non_locked_field]
        credentials_non_expired = request_json[self.__credentials_non_expired_field]
        enabled = request_json[self.__enabled_field]

        user_db = UserDB(storage_service=self.__db_storage_service, uuid=user_uuid, email=email,
                         password=password, account_non_expired=account_non_expired,
                         account_non_locked=account_non_locked, credentials_non_expired=credentials_non_expired,
                         enabled=enabled)
        user_db.update()

        resp = make_response("", 200)
        resp.headers['Location'] = '%s/%s/uuid/%s' % (cfg.API_BASE_URI, self.__api_url__, uuid)
        return resp

    def get(self, uuid: str = None, email: str = None) -> Response:
        if uuid is not None:
            try:
                uuidlib.UUID(uuid)
            except ValueError as e:
                message = 'User not found'
                developer_message = 'Bad uuid value.'
                system_error_code = AuthError.USER_FINDBYUUID_ERROR
                logging.error(e)
                data_err = {
                    'system_error_code': system_error_code,
                    'developer_message': developer_message
                }
                data = {
                    'error': {
                        'code': system_error_code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 404)
                return resp
        user_db = UserDB(storage_service=self.__db_storage_service, uuid=uuid, email=email)
        if uuid is None and email is None:
            # find all user is no parameter set
            try:
                user_list = user_db.find_all()
                resp = make_response(json.dumps([ob.to_dict() for ob in user_list], cls=JSONDecimalEncoder), 200)
            except UserException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 404)
            return resp
        elif uuid is not None:
            # find user by uuid
            try:
                user = user_db.find_by_uuid()
                resp = make_response(json.dumps(user.to_dict(), cls=JSONDecimalEncoder), 200)
            except UserNotFoundException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 404)
            except UserException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 500)
        elif email is not None:
            # find user by email
            try:
                user = user_db.find_by_email()
                resp = make_response(json.dumps(user.to_dict(), cls=JSONDecimalEncoder), 200)
            except UserNotFoundException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 404)
            except UserException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 500)
        else:
            data = {
                'error': {
                    'code': AuthError.UNKNOWN_ERROR_CODE,
                    'message': "UserAPI get method all parameters are null. WTF?"
                }
            }
            resp = make_response(json.dumps(data), 500)
        return resp
