from binanceposition.provider.supplier.BinancePositionSupplier import BinancePositionSupplier

if __name__ == '__main__':

    options = {
        'BINANCE_API_KEY': '<API-KEY>',
        'BINANCE_API_SECRET': '<API-SECRET>'
    }

    position_supplier = BinancePositionSupplier(options)
    positions = position_supplier.get_positions()
    print('positions are:')
    print('-----------------------')
    for position in positions:
        print(position)
