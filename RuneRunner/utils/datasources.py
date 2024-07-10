DATA_SOURCES = {
    'unisat': {
        'base_url': 'https://unisat.io',
        'endpoints': {
            'market_info': '/api/v1/market/info',
            'runes': '/api/v1/runes',
            'ordinals': '/api/v1/ordinals'
        }
    },
    'magiceden': {
        'base_url': 'https://api-mainnet.magiceden.io/v2',
        'endpoints': {
            'runes': '/runes',
            'ordinals': '/ordinals'
        }
    },
    'okx': {
        'base_url': 'https://www.okx.com/api/v5',
        'endpoints': {
            'market_data': '/market/tickers'
        }
    }
}