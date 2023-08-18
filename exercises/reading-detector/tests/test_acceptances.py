import pytest
from reading_detector import cli

from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_should_return_fraud_results(runner):
    result = runner.invoke(cli.main, ['./resources/2016-readings.csv'])
    assert result.output.strip().replace(
        ' ', '') == ('|Client|Month|Suspicious|Median|\n'
                     '|---------------|---------|--------------|----------|\n'
                     '|583ef6329d7b9|2016-09|3564|42798.5|\n'
                     '|583ef6329d89b|2016-09|162078|59606.5|\n'
                     '|583ef6329d89b|2016-10|7759|59606.5|\n'
                     '|583ef6329d916|2016-09|2479|40956|')
