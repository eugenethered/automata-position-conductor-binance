from typing import List

from binance.spot import Spot as Client
from core.number.BigFloat import BigFloat
from core.options.exception.MissingOptionError import MissingOptionError
from core.position.Position import Position
from coreutility.collection.dictionary_utility import as_data
from position.provider.supplier.PositionSupplier import PositionSupplier

BINANCE_API_KEY = 'BINANCE_API_KEY'
BINANCE_API_SECRET = 'BINANCE_API_SECRET'


class BinancePositionSupplier(PositionSupplier):

    def __init__(self, options):
        self.options = options
        self.__check_options()
        self.client = Client(self.options[BINANCE_API_KEY], self.options[BINANCE_API_SECRET])

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {BINANCE_API_KEY} and {BINANCE_API_SECRET}')
        if BINANCE_API_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {BINANCE_API_KEY}')
        if BINANCE_API_SECRET not in self.options:
            raise MissingOptionError(f'missing option please provide option {BINANCE_API_SECRET}')

    def get_positions(self) -> List[Position]:
        account_info = self.client.account()
        position_balances = account_info['balances']
        return self.extract_positions(position_balances)

    def extract_positions(self, position_balances) -> List[Position]:
        if position_balances is None or len(position_balances) == 0:
            return []
        parsed_positions = [position for position_balance in position_balances if (position := self.parse_position(position_balance)) is not None]
        return list(parsed_positions)

    def parse_position(self, position_balance):
        instrument = as_data(position_balance, 'asset')
        available_balance = BigFloat(as_data(position_balance, 'free', '0.00'))
        unavailable_balance = BigFloat(as_data(position_balance, 'locked', '0.00'))
        if self.is_position_available(available_balance, unavailable_balance):
            return Position(instrument=instrument, quantity=available_balance)

    @staticmethod
    def is_position_available(available_balance, unavailable_balance):
        return not available_balance.is_zero() and available_balance != unavailable_balance
