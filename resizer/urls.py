from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import ImageListView, UploadImageView, EditImageView

app_name = 'resizer'

urlpatterns = [
    path('', ImageListView.as_view(), name='main'),
    path('upload/', UploadImageView.as_view(), name='upload'),
    path('edit/<slug:image_hash>', EditImageView.as_view(), name='edit'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
