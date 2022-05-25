import logging
from typing import List

from binance.error import ClientError
from binance.spot import Spot as Client
from core.number.BigFloat import BigFloat
from core.position.Position import Position
from coreauth.AuthenticatedCredentials import AuthenticatedCredentials
from coreauth.exception.UnableToAuthenticateError import UnableToAuthenticateError
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
        try:
            self.lazy_init_client()
            account_info = self.client.account()
            event_time = account_info['updateTime']
            position_balances = account_info['balances']
            return self.extract_positions(position_balances, event_time)
        except ClientError as binance_client_error:
            self.log.warning(f'Unable to authenticate binance client, error:[{binance_client_error.error_message}]')
            raise UnableToAuthenticateError(binance_client_error.error_message)

    def extract_positions(self, position_balances, event_time) -> List[Position]:
        if position_balances is None or len(position_balances) == 0:
            return []
        parsed_positions = [position for position_balance in position_balances if (position := self.parse_position(position_balance, event_time)) is not None]
        return list(parsed_positions)

    def parse_position(self, position_balance, event_time):
        instrument = as_data(position_balance, 'asset')
        available_balance = BigFloat(as_data(position_balance, 'free', '0.00'))
        unavailable_balance = BigFloat(as_data(position_balance, 'locked', '0.00'))
        if self.is_position_available(available_balance, unavailable_balance):
            return Position(instrument=instrument, quantity=available_balance, instant=event_time)

    @staticmethod
    def is_position_available(available_balance, unavailable_balance):
        return not available_balance.is_zero() and available_balance != unavailable_balance
