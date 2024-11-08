from django.urls import path

from . import views
from .views import FileUploadView
# Define the URL patterns for the RhombusAI app
urlpatterns = [
	path('', views.index, name='index'),
	path('upload/', FileUploadView.as_view(), name='file-upload'),
]