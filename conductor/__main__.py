import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash
from core.environment.EnvironmentVariables import EnvironmentVariables
from logger.ConfigureLogger import ConfigureLogger

from conductor.BinancePositionConductor import BinancePositionConductor


def start():
    ConfigureLogger()

    environment_variables = EnvironmentVariables()

    log = logging.getLogger('Binance Position Conductor')
    log.info('position conductor initialized')

    RedisCacheHolder(environment_variables.options, held_type=RedisCacheProviderWithHash)

    conductor = BinancePositionConductor(environment_variables.options)
    conductor.start_process_schedule()


if __name__ == '__main__':
    start()
