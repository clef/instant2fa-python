def get_attributes_from_response(response):
    data = response.json().get('data')
    return data.get('attributes')


def construct_path(resource_type, method, lookup_key=None):
    if method == 'POST':
        return '/{}/'.format(resource_type)
    elif method == 'GET':
        return '/{}/{}'.format(resource_type, lookup_key)
    else:
        raise NotImplementedError('Method {} not supported.'.format(method))


def construct_request_body(resource_type, **kwargs):
    top_level = dict()
    data = dict(type=resource_type)
    attributes = dict()
    for k, v in kwargs.items():
        attributes[k] = v
    data['attributes'] = attributes
    top_level['data'] = data
    return top_level


def get_error_from_response(response):
    error = response.json().get('errors').pop()
    message = error.get('detail') or error.get('title')
    return message


def get_headers():
    return {'Content-Type': 'application/vnd.api+json'}
