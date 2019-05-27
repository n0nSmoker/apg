import logging
from urllib.parse import quote_plus

from config import EXAMPLE_API_DOMAIN

from .base import BaseAPI


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ExampleAPI')


class ExampleAPI(BaseAPI):
    domain = EXAMPLE_API_DOMAIN

    async def _request(self, url, auth_token=None, method='get', params=None, json=None):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        logger.info('url: %s, token: %s, method: %s, params: %s', url, auth_token, method, params)

        if auth_token:
            headers['X-Auth-Token'] = quote_plus(auth_token)

        return await self.fetch(
            method=method,
            url=f'{self.domain}{url}',
            params=params,
            json=json,
            headers=headers
        )

    # example methods
    async def example(self, int_field, str_field=''):
        # Uncomment this section for usage with proxy API
        # params = {
        #     'int': int_field,
        #     'str_field': str_field,
        #     'date_field': date_field,
        #     'datetime_field': datetime_field,
        # }
        # resp = await self._request(
        #     url='/example_api_endpoint_url',
        #     params=params
        # )
        # return resp

        result = dict(
            int_field=int_field,
            str_field=str_field,
        )

        return result

    async def example_json(self, kwargs):
        result = dict(
            **kwargs
        )
        return result

    async def example_update(self, item_id, int_field, str_field=''):
        result = dict(
            item_id=item_id,
            int_field=int_field,
            str_field=str_field,
        )

        return result

    async def example_delete(self, item_id):
        result = dict(
            item_id=item_id,
            message='successfully deleted'
        )

        return result
