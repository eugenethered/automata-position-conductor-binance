from cache.holder.RedisCacheHolder import RedisCacheHolder

from conductor.provider.supplier.BinancePositionSupplier import BinancePositionSupplier

if __name__ == '__main__':

    options = {
        'REDIS_SERVER_ADDRESS': '192.168.1.90',
        'REDIS_SERVER_PORT': 6379,
        'POSITION_KEY': 'test:position',
        'POSITION_HISTORY_LIMIT': 10,
        'AUTH_INFO_KEY': 'binance:auth:info'
    }

    RedisCacheHolder(options)

    position_supplier = BinancePositionSupplier(options)
    positions = position_supplier.get_positions()

    print('positions are:')
    print('-----------------------')
    for position in positions:
        print(position)
