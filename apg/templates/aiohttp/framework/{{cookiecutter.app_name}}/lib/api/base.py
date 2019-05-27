import json as ujson
import logging

from aiohttp.client_exceptions import ContentTypeError
from webargs.core import missing


logger = logging.getLogger()


class APIException(Exception):
    def __init__(self, meta=None, status=500): #noqa
        self.meta = meta
        self.status = status


class BaseAPI: #noqa
    SUCCESS_STATUS_CODE = (200, 204)

    def __init__(self, session):
        self.session = session

    async def fetch(self, url, method='get', params=None, data=None, json=None, headers=None): #noqa
        if params:
            fixed = {}
            for k, v in params.items():
                if isinstance(v, bool):
                    v = str(v).lower()
                elif v is None or v is missing:
                    continue
                fixed[k] = v
            params = fixed

        if json:
            json = {k: v for k, v in json.items() if v is not None and v is not missing}

        async with getattr(self.session, method)(url, params=params, data=data, json=json, headers=headers) as response: #noqa
            if response.status not in self.SUCCESS_STATUS_CODE:
                logger.error('API error: status=%s, url=%s', response.status, url)

                try:
                    resp = await response.json()
                except ContentTypeError:
                    resp = {}

                raise APIException(meta=resp.get('meta', resp), status=response.status)

            try:
                return await response.json()
            except ContentTypeError:
                text = await response.text()
                try:
                    return ujson.loads(text) if text else {}
                except ValueError:
                    return text
