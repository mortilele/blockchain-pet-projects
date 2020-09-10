from django.shortcuts import render
from core import constants
from pycoingecko import CoinGeckoAPI

client = CoinGeckoAPI()


async def dashboard(request):
    params = {
        'localization': 'false',
        'tickers': 'false',
        'market_data': 'true',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }

    ethereum_details = [client.get_coin_by_id(ethereum, **params) for ethereum in constants.ethereums_ids]

    context = {
        'etheriums_details': ethereum_details,
    }
    return render(request, 'base.html', context)
