from django.urls import path
from .views import upload, scanner
urlpatterns = [
	path('', upload, name='upload'),
	path('scanner/', scanner, name='scanner'),
]