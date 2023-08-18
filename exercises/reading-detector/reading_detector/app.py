"""Application model to represent Business logic."""
import abc

from typing import IO, List

from reading_detector.models import FraudResult


class MLPort(abc.ABC):
    """Port contract for ml service."""
    @abc.abstractmethod
    def run(self, fil: IO) -> List[FraudResult]:
        """Run ML code."""
        pass


class Application(object):
    """Constructor for application module."""

    def __init__(self, ml_adapter: MLPort):
        self._ml_adapter = ml_adapter

    def run_ml_detection(self, fil: IO) -> List[FraudResult]:
        """Main use case of the business logic where it call the ml_adapter.

        Args:
            fil (IO): File object with dataset inforomation.

        Results:
            List of possible fraud information.

        """
        return self._ml_adapter.run(fil)
