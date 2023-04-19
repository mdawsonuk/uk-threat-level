from uk_threat_level.threat_level import RSS_FEED_URL, ThreatLevel
from uk_threat_level.threat_levels import ThreatLevels

import responses


CLOUDFLARE_BOT_RESPONSE = """<!DOCTYPE html>
<html lang="en-US">
<head>
    <title>Just a moment...</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <meta name="robots" content="noindex,nofollow">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link href="/cdn-cgi/styles/challenges.css" rel="stylesheet">      
    

</head>
<body class="no-js">
    <div class="main-wrapper" role="main">
    <div class="main-content">
        <noscript>
            <div id="challenge-error-title">
                <div class="h2">
                    <span class="icon-wrapper">
                        <div class="heading-icon warning-icon"></div>
                    </span>
                    <span id="challenge-error-text">
                        Enable JavaScript and cookies to continue
                    </span>
                </div>
            </div>
        </noscript>
        <div id="trk_jschal_js" style="display:none;background-image:url('/cdn-cgi/images/trace/managed/nojs/transparent.gif')"></div>
        <form id="challenge-form" action="/UKThreatLevel/UKThreatLevel.xml" method="POST" enctype="application/x-www-form-urlencoded">
            <input type="hidden" name="md" value="">
        </form>
    </div>
</div>
<script>
    (function(){
        window._cf_chl_opt={
            cvId: '2',
            cZone: 'www.mi5.gov.uk',
            cType: 'managed',
            cNounce: '88565',
            cRay: '',
            cHash: '',
            cUPMDTk: "\/UKThreatLevel\/UKThreatLevel.xml",
            cFPWv: 'g',
            cTTimeMs: '1000',
            cMTimeMs: '0',
            cTplV: 5,
            cTplB: 'cf',
            cK: "",
            cRq: {
            }
        };
        var trkjs = document.createElement('img');
        trkjs.setAttribute('src', '/cdn-cgi/images/trace/managed/js/transparent.gif');
        trkjs.setAttribute('alt', '');
        trkjs.setAttribute('style', 'display: none');
        document.body.appendChild(trkjs);
        var cpo = document.createElement('script');
        cpo.src = '/cdn-cgi/challenge-platform/h/g/orchestrate/managed/v1';
        window._cf_chl_opt.cOgUHash = location.hash === '' && location.href.indexOf('#') !== -1 ? '#' : location.hash;
        window._cf_chl_opt.cOgUQuery = location.search === '' && location.href.slice(0, location.href.length - window._cf_chl_opt.cOgUHash.length).indexOf('?') !== -1 ? '?' : location.search;
        if (window.history && window.history.replaceState) {
            var ogU = location.pathname + window._cf_chl_opt.cOgUQuery + window._cf_chl_opt.cOgUHash;
            history.replaceState(null, null, "\/UKThreatLevel\/UKThreatLevel.xml" + window._cf_chl_opt.cOgUHash);
            cpo.onload = function() {
                history.replaceState(null, null, ogU);
            };
        }
        document.getElementsByTagName('head')[0].appendChild(cpo);
    }());
</script>
</body>
</html>"""

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


@responses.activate
def test_get_threat_level_status_error():
    tl = ThreatLevel()
    with responses.RequestsMock() as r:
        r.add(
            responses.GET, RSS_FEED_URL,
            status=403,
            body=CLOUDFLARE_BOT_RESPONSE,
        )
        assert tl.update_threat_levels() == False
        assert tl.was_retrieved() == False


@responses.activate
def test_get_threat_level_format_error():
    tl = ThreatLevel()
    with responses.RequestsMock() as r:
        r.add(
            responses.GET, RSS_FEED_URL,
            body=CLOUDFLARE_BOT_RESPONSE,
        )
        assert tl.update_threat_levels() == False
        assert tl.was_retrieved() == False
