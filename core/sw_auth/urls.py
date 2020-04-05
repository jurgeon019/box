from django.urls import path, include 
from .views import * 



def confirm(request):
    return render(request, 'core/confirm.html', locals())


urlpatterns = [
    path('', include('box.core.sw_auth.api.urls')),
    path('sw_logout/', sw_logout, name='sw_logout'),
    path('confirm/<uid>/<token>/', confirm),

]
