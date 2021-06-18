from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('cities', views.view_cities, name='cities-route'),
    path('city/<str:city>', views.city_weather, name='weather-route'),
    path('forecast/<str:city>', views.city_forecast, name='forecast-route'),
    path('upload/', views.create_city, name = 'upload-city'),
    path('update/<int:city_id>', views.update_city),
    path('delete/<int:city_id>', views.delete_city)
]
