from enum import Enum


class ThreatLevels(Enum):
    """
    Enum with all possible ThreatLevels.

    - LOW: an attack is highly unlikely
    - MODERATE: an attack is possible, but not likely
    - SUBSTANTIAL: an attack is likely
    - SEVERE: an attack is highly likely
    - CRITICAL: an attack is highly likely in the near future

    - UNKNOWN: the threat level has not yet been retrieved
    """
    LOW = "LOW"
    MODERATE = "MODERATE"
    SUBSTANTIAL = "SUBSTANTIAL"
    SEVERE = "SEVERE"
    CRITICAL = "CRITICAL"

    UNKNOWN = "UNKNOWN"
