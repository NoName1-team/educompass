from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomePageView, CategoryView

app_name = "main"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='categories'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
