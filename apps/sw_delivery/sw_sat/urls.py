# https://www.sat.ua/api/methods/main/
# https://www.sat.ua/api/methods/main/getrsp/
# https://www.sat.ua/api/methods/main/gettowns/


from django.urls import path, include 


sat_url = 'https://api.sat.ua/study/hs/api/v1.0/main/json/'

towns = f"{sat_url}getTowns?language=uk"

warehouses = f"{sat_url}getRsp?language=uk"







urlpatterns = [
    
]
