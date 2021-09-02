import os
from typing import Dict

import requests

from singleton import logger


URL_PREFIX = 'http://162.55.89.135:444/vv/hs/card/'

LOYALTY_BRAND = os.getenv("LOYALTY_BRAND")
AUTHZ_HEADER_VALUE = os.getenv("AUTHZ_HEADER_VALUE")
assert LOYALTY_BRAND in ('vivat', 'librarium')


def get_number_status(phone_number):
    headers = {'Authorization': AUTHZ_HEADER_VALUE}

    if LOYALTY_BRAND == 'vivat':
        url = "{}card_check?type=vivat&phone={}".format(URL_PREFIX, phone_number)
    elif LOYALTY_BRAND == 'librarium':
        url = "{}card_check?type=librarium&phone={}".format(URL_PREFIX, phone_number)

    logger.debug("Sending the following GET request: url = {}; headers = {}".format(url, headers))
    result = requests.get(url = url, headers = headers)

    json = result.json()
    logger.debug("Receiving the JSON response: {}".format(json))

    return json


def post_card_data(data: Dict):
    children = data.get('children')
    if children is not None:
        for child in children:
            day, month, year = child['date_birth'].split('.')
            child['date_birth'] = "{}{}{}".format(year, month, day)

    day, month, year = data['date_birth'].split('.')
    data['date_birth'] = "{}{}{}".format(year, month, day)

    if 'agreement' in data:
        data.pop('agreement')

    url = '{}card_data'.format(URL_PREFIX)

    headers = {'Authorization': AUTHZ_HEADER_VALUE}

    logger.debug("Sending the following POST request: url = {}; headers = {}; json = {}".format(url, headers, data))
    result = requests.post(url = url, headers = headers, json = data)

    try:
        logger.debug("Receiving the result raw: {}".format(result.raw))
        logger.debug("Receiving the result headers: {}".format(result.headers))
        logger.debug("Receiving the result json: {}".format(result.json()))
    except Exception:
        pass

    return result.status_code