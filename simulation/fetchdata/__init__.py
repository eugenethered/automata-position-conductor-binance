import logging
import time

from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash

from conductor.BinancePositionConductor import BinancePositionConductor

if __name__ == '__main__':

    options = {
        'REDIS_SERVER_ADDRESS': '10.104.71.60',
        'REDIS_SERVER_PORT': 6379,
        'POSITION_SLIP_KEY': 'test:position:slip',
        'POSITION_KEY': 'test:position',
        'POSITION_HISTORY_LIMIT': 10,
        'AUTH_INFO_KEY': 'binance:auth:info',
        'PROCESS_KEY': 'binance:process:mv:status',
        'PROCESS_RUN_PROFILE_KEY': 'binance:process:mv:run-profile'
    }

    logging.basicConfig(level=logging.DEBUG)

    RedisCacheHolder(options, held_type=RedisCacheProviderWithHash)

    start_time = time.perf_counter()

    conductor = BinancePositionConductor(options)
    conductor.run()

    end_time = time.perf_counter()
    print(f"Completed in {end_time - start_time:0.4f} seconds")
