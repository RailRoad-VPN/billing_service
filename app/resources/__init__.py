from typing import Any

from flask.views import MethodView


class API(MethodView):
    __version__ = 1

    _offset_field = 'offset'

    def __init__(self):
        pass

    def get(self, **kwargs) -> str:
        pass

    def post(self, **kwargs) -> bool:
        pass

    def delete(self, **kwargs) -> bool:
        pass

    def put(self, **kwargs) -> Any:
        pass