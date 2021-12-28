import requests
import json
import configs
from pathlib import Path
import re

def read_protocol_tvl(coin):
    """Uses the defillama API to read protocol TVL
    :param coin: This is the name of the protocol that can be obtained from https://api.llama.fi/protocols
    :return: protocol_tvl: This is the protocol's TVL in billions USD
    """

    configs.init()

    # The file technically is not a JSON, but I am limiting the number of extensions
    link = 'https://api.llama.fi/tvl/' + coin
    if (configs.DEV_MODE == 'OFF'):
        try:

            response = requests.get(link)
            if re.search('200', str(response)):
                response_text = response.text
                print(f'Defillama protocol endpoint: {link} {response}')
                if (reponse_text == '[]'):
                    raise Exception(f'Defillama {link} response: {response.text}')
            else:
                raise Exception(f'Defillama {link} response: {response.text}')

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    elif (configs.DEV_MODE == 'ON'):
        try:
            coin_file = configs.DATA_FILE_PATH + coin + '.json'
            coin_file_path = Path(coin_file)
        except:
            raise SystemExit('configs.DATA_FILE_PATH not defined')
        if (not coin_file_path.exists()):
            try:
                with open(coin_file, 'w', encoding='utf-8') as outfile:
                    try:
                        response = requests.get(link)
                        if re.search('200', str(response)):
                            response_text = response.text
                            print(f'defillama protocol endpoint: {link} {response}')
                        else:
                            raise Exception(f'Defillama {link} response: {response.text}')
                    except requests.exceptions.RequestException as e:
                        raise SystemExit(e)
                    outfile.write(response.text)
                    response_text = response.text
            except IOError as ioerror:
                raise SystemExit(ioerror)
        # else just read the saved files
        else:
            try:
                with open(coin_file, 'r', encoding='utf-8') as infile:
                    response_text = infile.read()
                    print(coin_file, ' exists')
            except IOError as ioerror:
                raise SystemExit(ioerror)

    protocol_tvl = float(response_text) / configs.UNIT

    return protocol_tvl


def read_chain_tvl(chain):
    """Uses the defillama API to read protocol TVL
        :param chain: This is the name of the chain that can be obtained from https://api.llama.fi/charts/<chain>
        ex: https://api.llama.fi/charts/Solana
        :return: chain_tvl: This is the protocol's TVL in billions USD
    """
    configs.init()
    link = 'https://api.llama.fi/charts/' + chain
    if (configs.DEV_MODE == 'OFF'):
        try:
            response = requests.get(link)
            if re.search('200', str(response)):
                print(f'Defillama chain endpoint: {link} {response}')
                response_text = response.text
                if response_text == '[]':
                    raise Exception(f'Defillama {link} response: {response.text}')
            else:
                # Keeping this in case the API adds 400, 500, etc. responses
                raise Exception(f'Defillama {link} response: {response.text}')
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    elif (configs.DEV_MODE == 'ON'):
        try:
            chain_file = configs.DATA_FILE_PATH + chain + '.json'
            chain_file_path = Path(chain_file)
        except:
            raise SystemExit('configs.DATA_FILE_PATH not defined')
        if (not chain_file_path.exists()):
            try:
                with open(chain_file, 'w', encoding='utf-8') as outfile:
                    try:
                        link = 'https://api.llama.fi/charts/' + chain
                        response = requests.get(link)
                        if re.search('200', str(response)):
                            print(f'defillama chain endpoint: {link} {response}')
                            response_text = response.text
                        else:
                            raise Exception(f'Defillama {link} response: {response.text}')
                    except requests.exceptions.RequestException as e:
                        raise SystemExit(e)
                    outfile.write(response_text)
            except IOError as ioerror:
                raise SystemExit(ioerror)

        # The chain API returns JSON with the following format with the most recent TVL at the end of the file
        # [{'date': POSIX datetime, "totalliquidityUSD": liquidity in dollars, }, {next newer date & TVL}, ...]
        else:
            try:
                with open(chain_file, 'r', encoding='utf-8') as infile:
                    print(chain_file, ' exists.')
                    response_text = infile.read()
            except IOError as ioerror:
                raise SystemExit(ioerror)

    chain_tvls = json.loads(response_text)
    chain_tvl = chain_tvls[len(chain_tvls) - 1]['totalLiquidityUSD'] / configs.UNIT

    return chain_tvl
