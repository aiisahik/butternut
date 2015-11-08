def basic_info(request):
    from django.conf import settings
    return {
        'LOCAL_ENV': settings.LOCAL_ENV,
        'STATIC_URL': settings.STATIC_URL,
    }

