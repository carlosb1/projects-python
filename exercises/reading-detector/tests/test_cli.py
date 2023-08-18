import pytest
from unittest.mock import MagicMock
from datetime import datetime

from click.testing import CliRunner

from reading_detector import cli
from reading_detector.models import FraudResult


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 1


def test_cli_should_return_1_when_it_is_a_file(runner):
    result = runner.invoke(cli.main, ['nofile'])
    assert result.exit_code == 1


def test_cli_should_return_fraud_results(runner):
    expected_value = [FraudResult(
        '0b', datetime(2016, 2, 1, 0, 0), 100000., 3000.)]
    cli.app.run_ml_detection = MagicMock(return_value=expected_value)
    result = runner.invoke(cli.main, ['./resources/test_correct.csv'])
    assert result.output.strip().replace(
        ' ', '') == ('|Client|Month|Suspicious|Median|\n|----------|---------'
                     '|--------------|----------|\n|0b|2016-02|100000|3000|')
