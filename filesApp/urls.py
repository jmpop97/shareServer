from django.urls import path
from filesApp import views

urlpatterns = [
    path("",views.FileUploader.as_view(),name="files")
]