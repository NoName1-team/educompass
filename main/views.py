from django.shortcuts import render


from django.views.generic import ListView
from django.db.models import Count
from .models import EduCenter, Course, Category, Events




class HomePageView(ListView):
    model = EduCenter
    template_name = 'index.html'
    context_object_name = 'edu_centers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(course_count=Count('edu_centers__courses')).order_by('-course_count')
        top_categories = categories[:4]  
        
        context['categories'] = categories
        context['top_categories'] = top_categories  
        context['courses'] = Course.objects.all()
        context['events'] = Events.objects.all()

        
        return context
    

class CategoryView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(course_count=Count('edu_centers__courses')).order_by('-course_count')
        top_categories = categories[:4]  
        
        

        context['categories'] = categories
        context['top_categories'] = top_categories  
        context['edu_centers'] = EduCenter.objects.all()

        context['events'] = Events.objects.all()
        return context