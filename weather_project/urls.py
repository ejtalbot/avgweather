from django.urls import include, path

urlpatterns = [
    path('weatheravg/', include('weatheravg.urls'))
]