from django.urls import path
from src import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('userRegistration', views.userRegistration, name='userRegistration'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('serviceBooking/', views.bookingService, name='serviceBooking'),
    path('pageNotFound', views.PageNotFound.as_view(), name="pageNotFound")
]
