EVE_IGB_HEADERS = [
    'HTTP_EVE_SERVERIP',
    'HTTP_EVE_CHARNAME',
    'HTTP_EVE_CHARID',
    'HTTP_EVE_CORPNAME',
    'HTTP_EVE_CORPID',
    'HTTP_EVE_ALLIANCENAME',
    'HTTP_EVE_ALLIANCEID',
    'HTTP_EVE_REGIONNAME',
    'HTTP_EVE_CONSTELLATIONNAME',
    'HTTP_EVE_SOLARSYSTEMNAME',
    'HTTP_EVE_STATIONNAME',
    'HTTP_EVE_STATIONID',
    'HTTP_EVE_CORPROLE',
    'HTTP_EVE_SHIPNAME',
    'HTTP_EVE_SHIPTYPEID',
    'HTTP_EVE_SHIPTYPENAME',
    'HTTP_EVE_SHIPID',
    'HTTP_EVE_SOLARSYSTEMID',
    'HTTP_EVE_WARFACTIONID',
]


class IGBMiddleware(object):
    """
    Middleware to detect the EVE IGB, and process the provided headers
    """

    def process_request(self, request):

        request.is_igb = False
        request.is_igb_trusted = False

        if 'EVE-IGB' in request.META.get('HTTP_USER_AGENT', ''):
            request.is_igb = True
            if request.META.get('HTTP_EVE_TRUSTED', 'No') == 'Yes':
                request.is_igb_trusted = True

                for header in EVE_IGB_HEADERS:
                    if header in request.META:
                        setattr(request, header.replace('HTTP_', '').lower(), request.META.get(header))

