from django.shortcuts import render
from core import constants
from pycoingecko import CoinGeckoAPI

client = CoinGeckoAPI()


async def dashboard(request):
    """
    Endpoint to render dashboard page
        1. Collect data about ethereum/ethereum-classic from api
        2. Render base.html, send context
        3. Return rendered HTML page
    """

    # Prepare request parameters of api
    params = {
        'localization': 'false',
        'tickers': 'false',
        'market_data': 'true',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }

    # For each ethereum(ETH, ETC) get detail data from api
    ethereum_details = [client.get_coin_by_id(ethereum, **params) for ethereum in constants.ethereums_ids]

    context = {
        'etheriums_details': ethereum_details,
    }
    # Render and return template
    return render(request, 'base.html', context)
