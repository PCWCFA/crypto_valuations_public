from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import configs
import re
import keys

def read_mc_fdmc(cmc_ids):
    """Using the ID from coinmarketcap.com, get the market cap and fully-diluted marketcap.

    :return:
       The coinmarketcap response data
    """
    # Use this URL for production data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    # Use this URL for initial testing. Note it does not have the complete data
    # url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    configs.init()
    keys.init()

    parameters = {
        'id': cmc_ids
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': keys.CMC_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        if re.search('200', str(response)):
            cmc_status = data['status']

            if (cmc_status['error_code'] == 0):
                print(f'coinmarketcap {url} {response}')
                return data['data']
            else:
                raise Exception(f'Got {cmc_status}')
        else:
            raise Exception(f'Got cointmarketcap.com response {response}')

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        SystemExit(e)
