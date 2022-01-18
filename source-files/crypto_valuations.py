import xlwings
import coinmarketcap
import defillama
import configs
import defillama_slugs
import cmc_api


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
    sheet = wb.sheets['Watchlist']

    if configs.UPDATE_CMC_REFERENCE_DATA == 'ON':
        cmc_api.get_cmc_ids()

    # Use range expansion to get the entire table starting at A2.
    # See the https://docs.xlwings.org/en/stable/datastructures.html.
    # The ndim=2 is needed. In case there is only row in the Excel, I still want to force the return to a
    # list of lists to make the rest of the code the same regardless of the number of rows.

    rng_in = sheet.range('A2').options(expand='table', ndim=2)

    # Check the Excel data for integrity
    try:
        for line in rng_in.value:
            # When the CMC ID is missing in the first row, the result is not CMC_ID = None. Xlwings instead only reads
            # the first column.
            if len(line) < 10:
                raise ValueError('The Excel contains a badly formatted line at ', line)
            # This is the check for cmc_id missing from all the other rows other than the first.
            elif line[1] == None:
                raise ValueError('The Excel does not have a CMC ID at  ', line)
    except ValueError as e:
        raise SystemExit(e)

    # Form the output list for MC, FDMC, and TVL
    rng_out_value = []
    for i in range(len(rng_in.value)):
        rng_out_value.append([1, 2, 3])

    row = 0
    cmc_ids = ''
    for coin_metrics in rng_in.value:
        # gather the cmc_ids because the cmc API /v1/cryptocurrency/quotes/latest supports grouping
        try:
            cmc_id = str(int(coin_metrics[1]))
            if not any(cmc_id):
                # I know I'm DRY, Definitely Repeating Myself, but one line as a check before using seems worth
                # the benefit.
                raise ValueError('CMC ID cannot be blank.')
            elif cmc_ids != '':
                cmc_ids = cmc_ids + ',' + cmc_id
            else:
                cmc_ids = cmc_id
        except ValueError as e:
            SystemExit(e)

        try:
            defillama_coin = coin_metrics[4]
            if not any(defillama_coin):
                raise ValueError(f'Defillama Protocol or Chain Name cannot be blank.')

            defillama_type = coin_metrics[3].lower()
            if defillama_type == 'protocol':
                tvl = defillama.read_protocol_tvl(defillama_coin)
            elif defillama_type == 'chain':
                tvl = defillama.read_chain_tvl(defillama_coin)
            elif defillama_type == 'na':
                tvl = 0
            else:
                raise ValueError(f'Defillama_type must be protocol, chain, or na. Instead got {defillama_type}')
        except ValueError as e:
            SystemExit(e)

        # Write the tvl.
        rng_out_value[row][2] = tvl

        # Call coinmarketcap once all the cmc_ids are collected in a comma-separated string.
        if row == len(rng_in.value) - 1:
            cmc_data = coinmarketcap.read_mc_fdmc(cmc_ids)
            # Write the mc and fdmc.
            for j in range(0, len(rng_in.value)):
                cmc_id = str(int(rng_in.value[j][1]))
                rng_out_value[j][0] = cmc_data[cmc_id]['quote']['USD']['market_cap'] / configs.UNIT
                rng_out_value[j][1] = cmc_data[cmc_id]['quote']['USD']['fully_diluted_market_cap'] / configs.UNIT
        row += 1

    # Write the rng_out_value to Excel.
    sheet.range('F2').value = rng_out_value
