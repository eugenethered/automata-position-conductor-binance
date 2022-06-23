import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash
from core.arguments.command_line_arguments import option_arg_parser
from logger.ConfigureLogger import ConfigureLogger
from metainfo.MetaInfo import MetaInfo

from conductor.BinancePositionConductor import BinancePositionConductor


def start():
    ConfigureLogger()

    meta_info = MetaInfo('persuader-technology-automata-position-conductor-binance')

    command_line_arg_parser = option_arg_parser(meta_info)
    args = command_line_arg_parser.parse_args()

    log = logging.getLogger('Binance Position Conductor')
    log.info('position conductor initialized')

    RedisCacheHolder(args.options, held_type=RedisCacheProviderWithHash)

    conductor = BinancePositionConductor(args.options)
    conductor.start_process_schedule()


if __name__ == '__main__':
    start()
