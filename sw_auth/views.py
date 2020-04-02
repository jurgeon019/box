from django.shortcuts import redirect 
from django.contrib.auth import logout




def sw_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', "/"))
