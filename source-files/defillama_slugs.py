import requests
import json
import xlwings
import configs
import binary_search

def get_protocols_and_chains():
    """Reads https://api.llama.fi/protocols for a list of protocol names. This list can then be used for data
    validation in Excel
    :param
        None
    :return:
        [num_protocols, num_protocols_matched, num_protocols_not_matched, num_protocols_in_error, num_chains,
            num_chains_matched, num_chains_not_matched, num_chains_in_error]
    """

    configs.init()

    # First update the protocols.
    link = "https://api.llama.fi/protocols"
    print('Getting Defillama protocol reference data from ', link)
    try:
        response = requests.get(link)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    defillama_protocols = json.loads(response.text)
    wb = xlwings.Book('crypto_valuations.xlsx')
    sheet_cmc_ids = wb.sheets['cmc_ids']
    cmc_rng_in = sheet_cmc_ids.range('A2').options(expand='table', ndim=2)
    cmc_rng_out = cmc_rng_in.value
    cmc_ids = []
    for n in cmc_rng_in.value:
        if n[0] != 'NA':
           cmc_ids.append(int(n[0]))

    num_protocols = len(defillama_protocols)
    num_protocols_matched = 0
    num_protocols_not_matched = 0
    num_protocols_in_error = 0

    for defillama_protocol in defillama_protocols:
        defillama_cmc_id = defillama_protocol['cmcId']
        if not(defillama_cmc_id is None or defillama_cmc_id == 'null'):
            cmc_index = binary_search.search(cmc_ids, int(defillama_cmc_id))

        if cmc_index != -2 and not(defillama_cmc_id is None or defillama_cmc_id == 'null'):
            # xlwings reads all numbers as floats, so need to convert back to int.
            cmc_rng_out[cmc_index][0] = int(cmc_rng_out[cmc_index][0])
            # defillama_cmc_id is the same as the cmc_id, but adding so the output self checks.
            cmc_rng_out[cmc_index][3] = int(defillama_cmc_id)
            if defillama_protocol['gecko_id'] != None:
                cmc_rng_out[cmc_index][4] = defillama_protocol['gecko_id']

            cmc_rng_out[cmc_index][5] = defillama_protocol['slug']
            cmc_rng_out[cmc_index][8] = defillama_protocol['tvl']/configs.UNIT
            num_protocols_matched += 1
        # Chains or protocols that do not have CMC IDs. Ex: Optimism, Arbitrum, and reverse-protocol
        elif (defillama_cmc_id is None or defillama_cmc_id == 'null') and defillama_protocol['slug'] != None:
            cmc_rng_out.append(['NA', 'NA', 'NA', 'NA', defillama_protocol['gecko_id'], \
            defillama_protocol['slug'], 'NA', 'NA', defillama_protocol['tvl']/configs.UNIT])
            num_protocols_not_matched += 1
        else:
            print('cmcId present but not matched: ', defillama_cmc_id, ' ', defillama_protocol['name'])
            num_protocols_in_error += 1


    # Now update the chains.
    link = 'https://api.llama.fi/chains'
    print('Getting Defillama chain reference data from ', link)
    try:
        response = requests.get(link)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    defillama_chains = json.loads(response.text)

    num_chains = len(defillama_chains)
    num_chains_matched = 0
    num_chains_not_matched = 0
    num_chains_in_error = 0

    for defillama_chain in defillama_chains:
        defillama_cmc_id = defillama_chain['cmcId']
        if not(defillama_cmc_id is None or defillama_cmc_id == 'null'):
            cmc_index = binary_search.search(cmc_ids, int(defillama_cmc_id))

        if cmc_index != -2 and not(defillama_cmc_id is None or defillama_cmc_id == 'null'):
            # xlwings reads all numbers as floats, so need to convert back to int.
            cmc_rng_out[cmc_index][0] = int(cmc_rng_out[cmc_index][0])
            # defillama_cmc_id is the same as the cmc_id, but adding so the output self checks.
            cmc_rng_out[cmc_index][3] = int(defillama_cmc_id)
            # Chains don't have Gecko IDs, so column 4 is not updated
            cmc_rng_out[cmc_index][5] = defillama_chain['name'] # Chains have names but not slugs.
            cmc_rng_out[cmc_index][8] = defillama_chain['tvl']/configs.UNIT
            num_chains_matched += 1
        # Chains or protocols that do not have CMC IDs. Ex: Optimism, Arbitrum, and reverse-protocol
        elif (defillama_cmc_id is None or defillama_cmc_id == 'null') and defillama_chain['name'] != None:
            cmc_rng_out.append(['NA', 'NA', 'NA', 'NA', 'NA', \
                                defillama_chain['name'], 'NA', 'NA', defillama_chain['tvl']/configs.UNIT])
            num_chains_not_matched += 1
        else:
            print('cmcId present but not matched: ',  defillama_cmc_id, ' ', defillama_chain['name'])
            num_chains_in_error += 1

    # Xlwings reads all ints as floats, so re-write all the CMC_IDs as ints.
    for i, cmc_rng_out_line in enumerate(cmc_rng_out):
        if cmc_rng_out_line[0] != 'NA':
            cmc_rng_out[i][0] = int(cmc_rng_out_line[0])
        if len(cmc_rng_out_line) != 9:
            print(cmc_rng_out_line)

    sheet_cmc_ids.range('A2').value = cmc_rng_out

    return [num_protocols, num_protocols_matched, num_protocols_not_matched, num_protocols_in_error, num_chains,
            num_chains_matched, num_chains_not_matched, num_chains_in_error]