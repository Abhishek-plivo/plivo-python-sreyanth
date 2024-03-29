# -*- coding: utf-8 -*-
from plivo.utils import to_param_dict
from plivo.utils.validators import *

from ..base import ListResponseObject, PlivoResource, PlivoResourceInterface


class Endpoint(PlivoResource):
    _name = 'Endpoint'
    _identifier_string = 'endpoint_id'

    @validate_args(
        password=[of_type(six.text_type)],
        alias=[of_type(six.text_type)],
        app_id=[optional(of_type(six.text_type))])
    def update(self, password=None, alias=None, app_id=None):
        params = to_param_dict(self.update, locals())
        self.__dict__.update(params)
        return self.client.endpoints.update(self.id, **params)

    def delete(self):
        return self.client.endpoints.delete(self.id)


class Endpoints(PlivoResourceInterface):
    _resource_type = Endpoint

    @validate_args(
        username=[of_type(six.text_type)],
        password=[of_type(six.text_type)],
        alias=[of_type(six.text_type)],
        app_id=[optional(of_type(six.text_type))])
    def create(self, username, password, alias, app_id=None):
        return self.client.request('POST', ('Endpoint', ),
                                   to_param_dict(self.create, locals()))

    @validate_args(endpoint_id=[of_type(six.text_type)])
    def get(self, endpoint_id):
        return self.client.request('GET', ('Endpoint', endpoint_id))

    def list(self):
        return self.client.request(
            'GET',
            ('Endpoint', ),
            objects_type=Endpoint,
            response_type=ListResponseObject, )

    @validate_args(
        endpoint_id=[of_type(six.text_type)],
        password=[optional(of_type(six.text_type))],
        alias=[optional(of_type(six.text_type))],
        app_id=[optional(of_type(six.text_type))])
    def update(self, endpoint_id, password=None, alias=None, app_id=None):
        return self.client.request('POST', ('Endpoint', endpoint_id),
                                   to_param_dict(self.update, locals()))

    @validate_args(endpoint_id=[of_type(six.text_type)])
    def delete(self, endpoint_id):
        return self.client.request('DELETE', ('Endpoint', endpoint_id))
