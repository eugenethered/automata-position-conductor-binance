import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.arguments.command_line_arguments import option_arg_parser

from conductor.BinancePositionConductor import BinancePositionConductor

if __name__ == '__main__':
    command_line_arg_parser = option_arg_parser()
    args = command_line_arg_parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info(f'Binance Position Conductor starting with OPTIONS {args.options}')

    RedisCacheHolder(args.options)

    position_conductor = BinancePositionConductor(args.options)
    position_conductor.conduct_position_fetch()