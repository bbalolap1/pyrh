import configparser

import requests

from Robinhood import Robinhood

def get_config(config_filename):
    """parse test config file

    Args:
        config_filename (str): path to config file

    Returns:
        (:obj:`configparser.ConfigParser`)

    """
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        allow_no_value=True,
        delimiters=('='),
        inline_comment_prefixes=('#')
    )

    with open(config_filename, 'r') as file:
        config.read_file(file)

    return config

def fetch_endpoint_directly(
        endpoint_name,
        config,
        **kwargs,
):
    """fetch endpoint directly from Robinhood

    Args:
        endpoint_name (str): endpoint name in RH class
        **kwargs (:obj:`dict`) args for endpoint

    Returns:
        (:obj:`dict`) JSON-parsed data from Robinhood endpoint

    """
    rh_object = Robinhood()
    address = rh_object.endpoints[endpoint_name]

    headers = {
        'User-Agent': config.get('FETCH', 'user_agent')
    }
    req = requests.get(
        address,
        headers=headers,
        params=kwargs
    )
    req.raise_for_status()
    return req.json()

def fetch_REST_directly(
        endpoint_name,
        arg_string,
        config
):
    """fetch REST endpoint (instead of ?arg1=val1&arg2=val2)

    Args:
        endpoint_name (str): endpoint name in RH class
        arg_string (str): additional args to pass onto endpoint
        config (:obj:`configparser.ConfigParser`, optional): config for args

    Returns:
        (:obj:`dict`) JSON-parsed data from Robinhood endpoint

    """
    rh_object = Robinhood()
    address = rh_object.endpoints[endpoint_name]

    address = address + arg_string + '/'
    headers = {
        'User-Agent': config.get('FETCH', 'user_agent')
    }
    req = requests.get(
        address,
        headers=headers
    )
    req.raise_for_status()
    return req.json()
