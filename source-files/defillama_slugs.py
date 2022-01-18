import requests
import json
import xlwings

def get_protocols():
    """Reads https://api.llama.fi/protocols for a list of protocol names. This list can then be used for data
    validation in Excel
    :param
        None
    :return:
        None
    """

    link = "https://api.llama.fi/protocols"
    print('Getting Defillama protocol reference data from: ', link)
    try:
        response = requests.get(link)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    defillama_protocols = json.loads(response.text)

    wb = xlwings.Book('crypto_valuations.xlsx')
    sheet_dict = wb.sheets['Dictionary']

    defillama_reference_data = [[i] for i in range(len(defillama_protocols))]

    for i in range(0, len(defillama_protocols)):
        defillama_reference_data[i][0] = defillama_protocols[i]['name']

    sheet_dict.range('A2').options(expand='down').value = defillama_reference_data
    print('Number of defillama protocols written: ', len(defillama_protocols), '.')