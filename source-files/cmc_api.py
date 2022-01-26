from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import keys
import xlwings
import configs

def get_cmc_ids():
    """Reads https://pro-api.coinmarketcap.com/vi/cryptocurrency/map for a list of cryptocurrency symbols and IDs.
       This list can then be used as a data validation in Excel.
       :param
           None
       :return:
           None
       """
    keys.init()
    configs.init()

    # Use this URL for production data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

    # Use this URL for testing
    # url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/map'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': keys.CMC_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    print(f'Getting Coinmarketcap data from {url}')

    try:
        response = session.get(url)
        data = json.loads(response.text)
        cmc_ids_status = data['status']
        cmc_ids_data = data['data']
        cmc_ids_strs = []
        for i in range(0, configs.CMC_IDS_COUNT//configs.ID_REQUEST_LENGTH):
            cmc_ids_strs.extend(' ')

        cmc_ids_strs_count = 0

        if (cmc_ids_status['error_code'] == 0):
            try:
                # Open the workbook & watchlist.
                wb = xlwings.Book('crypto_valuations.xlsx')
                sheet_cmc_ids = wb.sheets['cmc_ids']

                # Empty the cmc_ids tab. This is needed because without, de-listed coins will continue to exist in
                # the Excel if their IDs happen to be greater than the highest CMC_ID currently listed.

                rng_out = sheet_cmc_ids.range('A2').options(expand='table', ndim=2).value
                for i in range(len(rng_out)):
                    rng_out[i] = ['', '', '', '', '', '', '', '', '', '']

                sheet_cmc_ids.range('A2').value = rng_out

                # initialize the cmc_reference_data
                cmc_reference_data = [[]]

                # Form the header of the reference data
                cmc_reference_data[0] = ['CMC ID', 'CMC Name', 'CMC Symbol', 'Defillama CmcId', 'Gecko ID', \
                                              'Defillama Slug', 'Market Cap', 'Fully-Diluted Market Cap', 'TVL']

                for i, cmc_ids_line in enumerate(cmc_ids_data):
                    # Writing a bunch of placeholders is a bit ugly, but it makes using xlwings range read in
                    # defilama_slugs.py and crypto_valuations.py so much easier because xlwings will grab a list of
                    # nine entries.
                    cmc_reference_data.append([str(cmc_ids_line['id']), cmc_ids_line['name'],
                                                    cmc_ids_line['symbol'], 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'])

                    # Form the list of cmc_ids_strs. Note that the endpoint quotes/latest has a limit of 800 quotes
                    # per aggregation. This is not a published limit but rather one I found by testing because when
                    # passed the entire list of cmc_ids, cmc gave a 414 response and text that the URL was too long.
                    if i > 0 and i % configs.ID_REQUEST_LENGTH == 0:
                        cmc_ids_strs_count += 1

                    if (cmc_ids_strs[cmc_ids_strs_count] == ' '):
                        cmc_ids_strs[cmc_ids_strs_count] = str(cmc_ids_line['id'])
                    else:
                        cmc_ids_strs[cmc_ids_strs_count] = (cmc_ids_strs[cmc_ids_strs_count] + ',' +
                                                            str(cmc_ids_line['id']))

                # Write the cmc_reference_data to the Excel
                sheet_cmc_ids.range('A1').value = cmc_reference_data

            except IOError as ioerror:
                raise SystemExit(ioerror)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return cmc_ids_strs
