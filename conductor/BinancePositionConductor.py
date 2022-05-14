from position.provider.PositionProvider import PositionProvider
from positionrepo.repository.PositionRepository import PositionRepository
from positionrepo.repository.PositionSlipRepository import PositionSlipRepository

from conductor.provider.supplier.BinancePositionSupplier import BinancePositionSupplier


class BinancePositionConductor:

    def __init__(self, options):
        self.options = options
        position_supplier = BinancePositionSupplier(options)
        position_repository = PositionRepository(options)
        position_slip_repository = PositionSlipRepository(options)
        self.position_provider = PositionProvider(position_supplier, position_repository, position_slip_repository)

    def conduct_position_fetch(self):
        # todo: need simple schedular
        self.position_provider.obtain_position()
