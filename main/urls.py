from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomePageView, CategoryView, CompaniesView, CourseView, search_courses
from . import views

app_name = "main"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('courses/', CourseView.as_view(), name='courses'),
    path('companies/', CompaniesView.as_view(), name='companies'),
    path('search/', views.ajax_search, name='ajax_search'),
    path('search-course/', search_courses, name='search_courses'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
