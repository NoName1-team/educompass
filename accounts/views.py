import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, TemplateView
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy

from main.models import Category, EduCenter




class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'auth/sign-up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Foydalanuvchi ma'lumotlarini sessiyaga saqlaymiz
            request.session['signup_data'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'phone': form.cleaned_data['phone'],
            }
            # Parol o'rnatish sahifasiga yo'naltirish
            return redirect('accounts:set-password')
        
        return render(request, 'auth/sign-up.html', {'form': form})


class SetPasswordView(View):
    def get(self, request):
        if 'signup_data' not in request.session:
            return redirect('accounts:sign-up')

        return render(request, 'auth/set-password.html')

    def post(self, request):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not password1 or not password2:
            return render(request, 'auth/set-password.html', {'error': 'Ikkala parolni ham kiriting'})

        if password1 != password2:
            return render(request, 'auth/set-password.html', {'error': 'Parollar mos kelmadi'})

        signup_data = request.session.get('signup_data')
        if signup_data:
            user = User(
                first_name=signup_data['first_name'],
                last_name=signup_data['last_name'],
                username=signup_data['phone'],
            )
            user.set_password(password1)
            user.is_active = True
            user.save()

            del request.session['signup_data']

            return redirect('accounts:entry')

        return render(request, 'auth/set-password.html', {'error': 'Xato yuz berdi, qayta urinib ko\'ring'})


class EntryView(ListView):
    model = Category
    template_name = 'entry.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # O'quv markazlarini kategoriyaga mos ravishda sanab chiqamiz
        categories_with_center_count = []
        for category in context['categories']:
            center_count = EduCenter.objects.filter(categories=category).count()
            categories_with_center_count.append({
                'category': category,
                'center_count': center_count
            })

        context['categories_with_center_count'] = categories_with_center_count
        return context

    def post(self, request, *args, **kwargs):
        selected_categories = request.POST.getlist('categories')

        # Faqat ikki kategoriya tanlash uchun tekshiruv
        if len(selected_categories) > 2:
            return self.render_to_response(self.get_context_data(error='Siz faqat ikki kategoriyani tanlashingiz mumkin'))

        # Keyingi sahifaga o'tkazamiz
        return redirect('accounts:pop_up', selected_categories=",".join(selected_categories))


class PopUpView(TemplateView):
    template_name = 'pop-up.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_categories = kwargs.get('selected_categories')
        

        selected_categories_list = selected_categories.split(',') if selected_categories else []
        
        context['selected_categories'] = selected_categories_list
        return context





API_KEY = 'ONDt6RV8Hmccgsw0a3qDZzRirUZ7R0qHNa3KAgMV'


class QuizView(View):
    template_name = 'test.html'

    def get(self, request):
        # Fetch 10 English questions from QuizAPI
        response = requests.get(
            'https://quizapi.io/api/v1/questions',
            headers={'X-Api-Key': API_KEY},
            params={'limit': 10, 'category': 'English'}  # English-related questions
        )
        
        if response.status_code == 200:
            quiz_data = response.json()  # Get quiz data from API
            return render(request, self.template_name, {'quiz_data': quiz_data})
        else:
            return render(request, self.template_name, {'error': 'Error fetching quiz data'})



class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True  
    next_page = reverse_lazy('main:home') 

    def get_success_url(self):
        return self.get_redirect_url() or self.next_page