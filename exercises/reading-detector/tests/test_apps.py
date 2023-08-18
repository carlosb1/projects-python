from unittest.mock import MagicMock
from datetime import datetime

from reading_detector.models import FraudResult
from reading_detector.adapters import FraudDetectorAdapter
from reading_detector.app import Application


def test_should_call_correctly_ml_adapter():
    expected_value = [FraudResult(
        '0b', datetime(2016, 2, 1, 0, 0), 100000., 3000.)]
    ml_adapter = FraudDetectorAdapter()
    ml_adapter.run = MagicMock(return_value=expected_value)
    app = Application(ml_adapter)
    fil = open('./resources/test_correct.csv')
    result = app.run_ml_detection(fil)
    assert (str(expected_value) == str(result))
