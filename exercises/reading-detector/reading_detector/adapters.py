"""Implementation for adapters for hexagonal architecture."""
from typing import IO, List
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

from reading_detector.models import FraudResult
from reading_detector.app import MLPort

GLOBAL_THRESHOLD: float = 10000.
INDIVIDUAL_THRES: float = 1.7


class FraudDetectorAdapter(MLPort):
    """Fraud class detector."""

    def run(self, fil: IO) -> List[FraudResult]:
        """
            From a csv file, it calculates possible fraud.

        Args:
            fil (IO): file object with csv information
        Returns:
            List of fraud information.

        """
        if not fil:
            return []
        info_path = Path(fil.name)
        if not info_path.suffix == '.csv':
            raise ValueError('It is a csv file path')
        data = pd.read_csv(fil)
        suspis_results: List[FraudResult] = []
        for id_client, info in data.groupby('client'):
            info_reading = info['reading']
            std = np.std(info_reading)
            if std > GLOBAL_THRESHOLD:
                mn = np.mean(info_reading)
                median = np.median(info_reading)
                scores = ((info_reading - mn) / std)
                ipositions = scores[(scores > INDIVIDUAL_THRES) | (scores < -INDIVIDUAL_THRES)]
                suspic_entries = data.loc[ipositions.index]
                list_suspic = [row for _, row in suspic_entries.iterrows()]
                suspis_results_by_client = [FraudResult(
                    sus['client'], datetime.strptime(sus['period'], '%Y-%m'), float(sus['reading']),
                    float(median)) for sus in list_suspic]
                suspis_results.extend(suspis_results_by_client)
        return suspis_results


class FraudDetectorAdapterV2(MLPort):
    """Fraud class detector."""

    def run(self, fil: IO) -> List[FraudResult]:
        """
            From a csv file, it calculates possible fraud folling exercise criteria.

        Args:
            fil (IO): file object with csv information
        Returns:
            List of fraud information.

        """
        if not fil:
            return []
        info_path = Path(fil.name)
        if not info_path.suffix == '.csv':
            raise ValueError('It is a csv file path')
        data = pd.read_csv(fil)
        suspis_results: List[FraudResult] = []
        for id_client, info in data.groupby('client'):
            info_year = info.groupby(info.period.map(
                lambda x: datetime.strptime(str(x), "%Y-%m").year))
            for date, info_data in info_year:
                info_reading_by_year = info_data['reading']
                median = np.median(info_reading_by_year)
                low_fil = median - median * .5
                high_fil = median + median * .5
                ipositions = info_reading_by_year[(info_reading_by_year < low_fil) | (
                    info_reading_by_year > high_fil)]
                suspic_entries = data.loc[ipositions.index]
                list_suspic = [row for _, row in suspic_entries.iterrows()]
                suspis_results_by_client = [FraudResult(sus['client'],
                                                        datetime.strptime(sus['period'], '%Y-%m'),
                                                        float(sus['reading']),
                                                        float(median)) for sus in list_suspic]
                suspis_results.extend(suspis_results_by_client)
        return suspis_results
