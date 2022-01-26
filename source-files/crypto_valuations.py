import xlwings
import coinmarketcap
import configs
import defillama_slugs
import cmc_api
import binary_search


def main():
    """Catches the call from xlwings' Excel plugin's Run main button for an Excel named the same as this Python

    :param:
        None

    :return:
        None
    """

    # init the global configs
    configs.init()

    # Open the workbook & watchlist
    wb = xlwings.Book('crypto_valuations.xlsx')
    sheet_cmc_ids = wb.sheets['cmc_ids']
    rng_in = sheet_cmc_ids.range('A2').options(expand='table', ndim=2)
    rng_out_value = rng_in.value

    # Get all listed coins from Coinmarketcap. Get also all protocols and chains from Defillama and match them up
    # to the list from Coinmarketcap using the cmc_id.
    cmc_ids_strs = cmc_api.get_cmc_ids()
    defillama_slugs.get_protocols_and_chains()

    rng_in_cmc_ids = []
    for n in rng_in.value:
        if (n[0] != 'NA'):
            rng_in_cmc_ids.append(int(n[0]))

    for j, cmc_ids_str in enumerate(cmc_ids_strs):
        # Get the market cap and fully-diluted market cap plus other coin data from coinmarketcap
        cmc_data = coinmarketcap.read_mc_fdmc(cmc_ids_str)
        cmc_ids_list = cmc_ids_str.split(',')

        # Then write the fully updated coin metrics back to crypto_valuations.xlsx
        for cmc_id in cmc_ids_list:
            cmc_index = binary_search.search(rng_in_cmc_ids, int(cmc_id))

            rng_out_value[cmc_index][0] = cmc_id
            rng_out_value[cmc_index][6] = cmc_data[cmc_id]['quote']['USD']['market_cap']/configs.UNIT
            rng_out_value[cmc_index][7] = cmc_data[cmc_id]['quote']['USD']['fully_diluted_market_cap']/configs.UNIT

    print('Updating crypto_valuations.xlsx')
    sheet_cmc_ids.range('A2').value = rng_out_value
