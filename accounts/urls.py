from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, CustomLoginView, SetPasswordView, EntryView, PopUpView, QuizView

app_name = "accounts"

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('entry/', EntryView.as_view(), name='entry'),
    path('popup/<str:selected_categories>/', PopUpView.as_view(), name='pop_up'),
    path('set-password/', SetPasswordView.as_view(), name='set-password'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('quiz/', QuizView.as_view(), name='quiz_page'),  
]
