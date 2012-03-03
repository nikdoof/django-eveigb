def igb(request):
    return {
        'is_igb': request.is_igb,
        'is_igb_trusted': request.is_igb_trusted,
    }

