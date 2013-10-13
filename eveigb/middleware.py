from django.conf import settings

# List of IGB headers, their type, and if they're expected in a all requests
EVE_IGB_HEADERS = [
    ('HTTP_EVE_SERVERIP', False, 'str'),
    ('HTTP_EVE_CHARNAME', True, 'str'),
    ('HTTP_EVE_CHARID', True, 'int'),
    ('HTTP_EVE_CORPNAME', True, 'str'),
    ('HTTP_EVE_CORPID', True, 'int'),
    ('HTTP_EVE_ALLIANCENAME', False, 'str'),
    ('HTTP_EVE_ALLIANCEID', False, 'int'),
    ('HTTP_EVE_REGIONNAME', True, 'str'),
    ('HTTP_EVE_CONSTELLATIONNAME', True, 'str'),
    ('HTTP_EVE_SOLARSYSTEMNAME', True, 'str'),
    ('HTTP_EVE_STATIONNAME', False, 'str'),
    ('HTTP_EVE_STATIONID', False, 'int'),
    ('HTTP_EVE_CORPROLE', True, 'int'),
    ('HTTP_EVE_SHIPNAME', True, 'str'),
    ('HTTP_EVE_SHIPTYPEID', True, 'int'),
    ('HTTP_EVE_SHIPTYPENAME', True, 'str'),
    ('HTTP_EVE_SHIPID', True, 'int'),
    ('HTTP_EVE_SOLARSYSTEMID', True, 'int'),
    ('HTTP_EVE_WARFACTIONID', False, 'int'),
]


class IGBMiddleware(object):
    """
    Middleware to detect the EVE IGB, and process the provided headers
    """

    def process_request(self, request):

        request.is_igb = False
        request.is_igb_trusted = False

        if 'EVE-IGB' in request.META.get('HTTP_USER_AGENT', ''):
            if getattr(settings, 'EVEIGB_SECURE_HEADERS', False):
                for hdr, req, typ in EVE_IGB_HEADERS:
                    if not req:
                        continue
                    if not hdr in request.META:
                        return
                    if typ == 'int':
                        try:
                            long(request.META.get(hdr))
                        except ValueError:
                            return
            request.is_igb = True
            if request.META.get('HTTP_EVE_TRUSTED', 'No') == 'Yes':
                request.is_igb_trusted = True

                for header, req, typ in EVE_IGB_HEADERS:
                    if header in request.META:
                        setattr(request, header.replace('HTTP_', '').lower(), request.META.get(header))

