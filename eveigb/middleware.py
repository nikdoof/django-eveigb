class IGBMiddleware(object):
    """
    Middleware to detect the EVE IGB
    """

    def process_request(self, request):

        request.is_igb = False
        request.is_igb_trusted = False

        header_map = [
            ('HTTP_EVE_SERVERIP', 'eve_server_ip'),
            ('HTTP_EVE_CHARNAME', 'eve_charname'),
            ('HTTP_EVE_CHARID', 'eve_charid'),
            ('HTTP_EVE_CORPNAME', 'eve_corpname'),
            ('HTTP_EVE_CORPID', 'eve_corpid'),
            ('HTTP_EVE_ALLIANCENAME', 'eve_alliancename'),
            ('HTTP_EVE_ALLIANCEID', 'eve_allianceid'),
            ('HTTP_EVE_REGIONNAME', 'eve_regionid'),
            ('HTTP_EVE_CONSTELLATIONNAME', 'eve_constellationname'),
            ('HTTP_EVE_SOLARSYSTEMNAME', 'eve_systemname'),
            ('HTTP_EVE_STATIONNAME', 'eve_stationname'),
            ('HTTP_EVE_STATIONID', 'eve_stationid'),
            ('HTTP_EVE_CORPROLE', 'eve_corprole'),
            ('HTTP_EVE_SHIPNAME', 'eve_shipname'),
            ('HTTP_EVE_SHIPTYPEID', 'eve_shiptypeid'),
            ('HTTP_EVE_SHIPTYPENAME', 'eve_shiptypename'),
            ('HTTP_EVE_SHIPID', 'eve_shipid'),
            ('HTTP_EVE_SOLARSYSTEMID', 'eve_systemid'),
            ('HTTP_EVE_WARFACTIONID', 'eve_warfactionid'),
        ]

        if 'EVE-IGB' in request.META.get('HTTP_USER_AGENT', ''):
            request.is_igb = True
            if request.META.get('HTTP_EVE_TRUSTED', 'No') == 'Yes':
                request.is_igb_trusted = True

                for header, map in header_map:
                    if request.META.get(header, None):
                        setattr(request, map, request.META.get(header, None))


def igb(request):
    return {
        'is_igb': request.is_igb,
        'is_igb_trusted': request.is_igb_trusted,
    }

