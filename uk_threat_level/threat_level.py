from enum import Enum

import feedparser
import re
import requests

RSS_FEED_URL = "https://www.mi5.gov.uk/UKThreatLevel/UKThreatLevel.xml"

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


class ThreatLevel:

    def __init__(self):
        self.retrieved = False
        self.threat_uk = ThreatLevels.UNKNOWN
        self.threat_ni = ThreatLevels.UNKNOWN
        self.last_updated = None
    
    def update_threat_levels(self) -> bool:
        raw_feed = requests.get(RSS_FEED_URL)

        parsed_feed = feedparser.parse(raw_feed.text)

        current_threat_level = parsed_feed.entries[0].summary_detail.value

        # Get all text results for capitalised words within the description
        # This will be in the format:
        # "The current national threat level is <LEVEL>. The threat to Northern Ireland from Northern Ireland-related terrorism is <LEVEL>.""
        (uk, ni) = re.findall(r"(\b[A-Z][A-Z]+|\b[A-Z]\b)", current_threat_level)

        self.threat_uk = ThreatLevels(uk)
        self.threat_ni = ThreatLevels(ni)
        self.retrieved = True

        return True

    def get_threat_level_uk(self) -> ThreatLevels:
        return self.threat_uk
    
    def get_threat_level_ni(self) -> ThreatLevels:
        return self.threat_ni
    
    def was_retrieved(self) -> bool:
        return self.was_retrieved
