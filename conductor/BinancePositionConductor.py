from position.provider.PositionProvider import PositionProvider
from positionrepo.repository.PositionRepository import PositionRepository
from positionrepo.repository.PositionSlipRepository import PositionSlipRepository
from processmanager.ScheduledProcess import ScheduledProcess

from conductor.provider.supplier.BinancePositionSupplier import BinancePositionSupplier


class BinancePositionConductor(ScheduledProcess):

    def __init__(self, options):
        super().__init__(options, 'binance', 'position-conductor')
        self.options = options
        position_supplier = BinancePositionSupplier(options)
        position_repository = PositionRepository(options)
        position_slip_repository = PositionSlipRepository(options)
        self.position_provider = PositionProvider(position_supplier, position_repository, position_slip_repository)

    def process_to_run(self):
        self.position_provider.updating_position()
        self.log.info('Position call complete')
