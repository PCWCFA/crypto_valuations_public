from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import keys
import xlwings

def get_cmc_ids():
    """Reads https://pro-api.coinmarketcap.com/vi/cryptocurrency/map for a list of cryptocurrency symbols and IDs.
       This list can then be used as a data validation in Excel.
       :param
           None
       :return:
           None
       """
    keys.init()

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

    try:
        response = session.get(url)
        data = json.loads(response.text)
        cmc_ids_status = data['status']
        cmc_ids_data = data['data']

        if (cmc_ids_status['error_code'] == 0):
            try:
                # Open the workbook & watchlist.
                wb = xlwings.Book('crypto_valuations.xlsx')
                sheet_cmc_ids = wb.sheets['cmc_ids']

                # initialize the cmc_reference_data
                cmc_reference_data = []
                for i in range(len(cmc_ids_data)+1):
                    cmc_reference_data.append(['1', '2', '3'])

                row = 0
                # Form the header of the reference data
                cmc_reference_data[row][0] = 'ID'
                cmc_reference_data[row][1] = 'Name'
                cmc_reference_data[row][2] = 'Symbol'
                row += 1

                # Iterate through the CMC reference data.
                i = 0
                while i < len(cmc_ids_data):
                   cmc_reference_data[row][0] = str(cmc_ids_data[i]['id'])
                   cmc_reference_data[row][1] = cmc_ids_data[i]['name']
                   cmc_reference_data[row][2] = cmc_ids_data[i]['symbol']
                   i += 1
                   row += 1

                # Write the cmc_reference_data to the Excel
                sheet_cmc_ids.range('A1').value = cmc_reference_data

            except IOError as ioerror:
                raise SystemExit(ioerror)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
