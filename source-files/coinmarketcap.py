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

    cmc_ids_list =  cmc_ids.split(',')

    try:
        response = session.get(url, params=parameters)

        if re.search('200', str(response)):
            data = json.loads(response.text)
            cmc_status = data['status']

            if (cmc_status['error_code'] == 0):
                print(f'Coinmarketcap mc and fdmc {url} {response} for cmc_ids {cmc_ids_list[0]} '
                      f'to {cmc_ids_list[len(cmc_ids_list) - 1]}')
                return data['data']
            else:
                raise Exception(f'Got {cmc_status}')
        else:
            raise Exception(f'Got cointmarketcap.com response {response} and {response.text}')

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        SystemExit(e)
