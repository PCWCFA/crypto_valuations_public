def init():
    global UNIT, ID_REQUEST_LENGTH, CMC_IDS_COUNT
    UNIT = 1000000000  # billion
    ID_REQUEST_LENGTH = 800 # How many cmc_ids to aggregate for calling Coinmarketcap's quotes/latest endupoint.
    CMC_IDS_COUNT = 10000 # This is the number of coin listed on Coinmarketcap as of Jan 2022.
