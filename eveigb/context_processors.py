def igb(request):
    ctx = {
        'is_igb': request.is_igb,
        'is_igb_trusted': request.is_igb_trusted,
    }
    return ctx
