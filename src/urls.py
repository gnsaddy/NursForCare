from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from src import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('userRegistration/', views.userRegistration, name='userRegistration'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('serviceBooking/', views.bookingService, name='serviceBooking'),
    path('vendorRegistration/', views.vendorRegistration, name="vendorRegistration"),
    path('patientProfile/', views.patientProfile, name="patientProfile"),
    path('patientStatus/', views.patientStatus, name="patientStatus"),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-services/', views.load_services, name='ajax_load_services'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
