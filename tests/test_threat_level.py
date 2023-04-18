from uk_threat_level.threat_level import RSS_FEED_URL, ThreatLevel
from uk_threat_level.threat_levels import ThreatLevels

import responses


def format_response(uk: ThreatLevels, ni: ThreatLevels) -> str:
    return f"""<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0" xml:base="https://www.mi5.gov.uk/">
    <channel>
    <title>Threat Level</title>
    <link>https://www.mi5.gov.uk/</link>
    <description>The Current UK Threat Level</description>
    <language>en-gb</language>
    <copyright>© Crown Copyright</copyright>
    <generator>MI5</generator>
    <webMaster>/</webMaster>
    <lastBuildDate>Tue, 22 Mar 2022 13:57:52 +0000</lastBuildDate>
    <ttl>20</ttl>
    <item>
    <title>Current Threat Level: SUBSTANTIAL</title>
    <link>https://www.mi5.gov.uk/threat-levels</link>
    <description>The current national threat level is {uk.value}. The threat to Northern Ireland from Northern Ireland-related terrorism is {ni.value}.</description>
    <pubDate>Tuesday, March 22, 2022 - 13:57</pubDate>
    <subject>ThreatLevel</subject>
    </item>
    </channel>
    </rss>"""

@responses.activate
def test_get_threat_level_uk():
    tl = ThreatLevel()
    with responses.RequestsMock() as r:
        r.add(
            responses.GET, RSS_FEED_URL,
            body=format_response(ThreatLevels.SUBSTANTIAL, ThreatLevels.UNKNOWN),
            status=200,
            content_type="text/xml; charset=utf-8"
        )
        assert tl.update_threat_levels() == True
        assert tl.was_retrieved() == True
        assert tl.get_threat_level_uk() == ThreatLevels.SUBSTANTIAL

@responses.activate
def test_get_threat_level_ni():
    tl = ThreatLevel()
    with responses.RequestsMock() as r:
        r.add(
            responses.GET, RSS_FEED_URL,
            body=format_response(ThreatLevels.UNKNOWN, ThreatLevels.SEVERE),
        )
        assert tl.update_threat_levels() == True
        assert tl.was_retrieved() == True
        assert tl.get_threat_level_ni() == ThreatLevels.SEVERE
