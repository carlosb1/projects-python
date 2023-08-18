import pytest
from datetime import datetime

from reading_detector.adapters import FraudDetectorAdapterV2, FraudDetectorAdapter
from reading_detector.models import FraudResult


@pytest.fixture
def detector():
    return FraudDetectorAdapter()


@pytest.fixture
def detectorv2():
    return FraudDetectorAdapterV2()


def test_run_should_return_empty_values(detector):
    result = detector.run(None)
    assert(result == [])


def test_run_should_not_load_a_non_csv_file(detector):
    with pytest.raises(ValueError):
        detector.run(open('resources/2016-readings.xml'))


def test_run_should_not_any_suspicious_value(detector):
    result = detector.run(open('resources/test_correct.csv'))
    assert(result == [])


def test_run_should_find_suspicious_value(detector):
    result = detector.run(open('resources/test_incorrect.csv'))
    assert(str(result) == str([FraudResult('0b', datetime(2016, 2, 1, 0, 0), 100000., 3000.)]))


def test_runv2_should_return_empty_values(detectorv2):
    result = detectorv2.run(None)
    assert(result == [])


def test_runv2_should_not_load_a_non_csv_file(detectorv2):
    with pytest.raises(ValueError):
        detectorv2.run(open('resources/2016-readings.xml'))


def test_runv2_should_not_any_suspicious_value(detectorv2):
    result = detectorv2.run(open('resources/test_correct.csv'))
    assert(result == [])


def test_runv2_should_find_suspicious_value(detectorv2):
    result = detectorv2.run(open('resources/test_incorrect.csv'))
    assert(str(result) == str([FraudResult('0b', datetime(2016, 2, 1, 0, 0), 100000., 3000.)]))
