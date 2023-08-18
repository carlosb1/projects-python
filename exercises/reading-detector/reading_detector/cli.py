"""Entrypoint to call a cli tool."""
import sys
from pathlib import Path
import click
import logging

from tabulate import tabulate

from reading_detector.adapters import FraudDetectorAdapterV2
from reading_detector.app import Application

# Inverse of dependencies to inject classes
fraud_detector = FraudDetectorAdapterV2()
app = Application(fraud_detector)


@click.command()
@click.argument('filepath', default='./readings.csv', required=True)
def main(filepath):
    """Exercise for HolaLuz for a fraud reading detector."""
    path = Path(filepath)

    if not path.is_file():
        click.echo('reading_detector filepath_csv')
        return sys.exit(1)
    try:
        fil = open(path)
        results = app.run_ml_detection(fil)
        headers = ['Client', 'Month', 'Suspicious', 'Median']
        output_result = [[result.client_id, result.month.strftime('%Y-%m'),
                          result.suspicious_reading, result.median]
                         for result in results]
        click.echo('{0}'.format(tabulate(output_result, headers=headers, tablefmt="github")))
    except IOError as err:
        logging.error(err, exc_info=True)
        click.echo("Input file is incorrect")
        return sys.exit(1)
