# coding=utf-8
import hashlib
import hmac
import uuid
from .compat import force_u, smart_b, quote, b_str, u_str, smart_u


def get_sign(secret, querystring=None, **params):
    """
    Return sign for querystring.

    Logic:
    - Sort querystring by parameter keys and by value if two or more parameter keys share the same name
    - URL encode sorted querystring
    - Generate a hex digested hmac/sha1 hash using given secret
    """
    if querystring:
        params = dict(param.split('=') for param in querystring.split('&'))
    sorted_params = []
    for key, value in sorted(params.items(), key=lambda x: x[0]):
        if isinstance(value, (b_str, u_str)):
            sorted_params.append((key, value))
        else:
            try:
                value = list(value)
            except TypeError as e:
                assert 'is not iterable' in smart_u(e)
                value = smart_b(value)
                sorted_params.append((key, value))
            else:
                sorted_params.extend((key, item) for item in sorted(value))
    return get_pairs_sign(secret, sorted_params)


def get_pairs_sign(secret, sorted_pairs):
    param_list = ('='.join((field, force_u(value))) for field, value in sorted_pairs)
    validation_string = smart_b('&'.join(param_list))
    validation_string = smart_b(quote(validation_string))
    return hmac.new(smart_b(secret), validation_string, hashlib.sha1).hexdigest()


def prepare_uuid_string(value, default=None):
    if isinstance(value, uuid.UUID):
        value = value.hex
    if not value:
        return default
    value = str(value).replace('-', '').strip().lower()
    return value
