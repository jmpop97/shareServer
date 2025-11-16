from django.urls import path
from filesApp import views
from django.views.static import serve
from .decorators import user_passes_test_with_path
from django.conf import settings
def permissionTest(user, path):
    print("USER:", user)
    print("PATH:", path)
    if path == "admin.jpg":
        if user.is_staff:
            return True
        else:
            return False
    return True

urlpatterns = [
    path("",views.FileUploader.as_view(),name="files"),
    path(
        "<path:path>",
        user_passes_test_with_path(permissionTest)(serve),
        {'document_root': settings.MEDIA_ROOT}
    ),
]