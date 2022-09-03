from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detections', views.ImageDetection.as_view()),
    path('upload-image', views.ocr_detect)
]
