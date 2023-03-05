from django.urls import path

from .views import home, main, restart

urlpatterns = [
    path('', home, name='home'),
    path('main/', main, name='main'),
    path('restart/', restart, name='restart'),
]
