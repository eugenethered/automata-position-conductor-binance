import logging
from typing import List

from binance.spot import Spot as Client
from core.number.BigFloat import BigFloat
from core.position.Position import Position
from coreauth.AuthenticatedCredentials import AuthenticatedCredentials
from coreutility.collection.dictionary_utility import as_data
from position.provider.supplier.PositionSupplier import PositionSupplier


class BinancePositionSupplier(PositionSupplier):

    def __init__(self, options):
        self.log = logging.getLogger(__name__)
        self.options = options
        (self.api_key, self.api_secret) = self.init_auth_credentials()
        self.client = None

    def init_auth_credentials(self):
        authenticated_credentials = AuthenticatedCredentials(self.options)
        api_key = authenticated_credentials.obtain_auth_value('API_KEY')
        api_secret = authenticated_credentials.obtain_auth_value('API_SECRET')
        return api_key, api_secret

    def lazy_init_client(self):
        if self.client is None:
            self.client = Client(self.api_key, self.api_secret)

    def get_positions(self) -> List[Position]:
        self.lazy_init_client()
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
