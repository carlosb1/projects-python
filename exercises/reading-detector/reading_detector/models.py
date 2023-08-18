"""Implementation of business classes."""
import datetime
from dataclasses import dataclass


@dataclass
class FraudResult:
    """
        Class to return fraud detection.

    Args:
        client_id (str): Client identifier.
        month (datetime): Fraud month.
        suspicious_reading (float): Number of the suspicious reading.
        median (float): Calculated median for user.

    """
    client_id: str
    month: datetime.datetime
    suspicious_reading: float
    median: float
