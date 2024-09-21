from django.shortcuts import render

from django.http import JsonResponse
from django.views.generic import ListView
from django.db.models import Count, Q
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

# main search 

def ajax_search(request):
    query = request.GET.get('q', '')

    centers_data = []
    courses_data = []

    if query:
        centers = EduCenter.objects.filter(
            Q(name__icontains=query) |
            Q(courses__name__icontains=query) |
            Q(courses__level__name__icontains=query)
        ).annotate(course_count=Count('courses')).distinct()

        for center in centers:
            center_courses = center.courses.filter(
                Q(name__icontains=query) |  
                Q(level__name__icontains=query)
            ).values('name', 'level__name')

            centers_data.append({
                'name': center.name,
                'location': center.location,
                'course_count': center.course_count,
                'logo': request.build_absolute_uri(center.logo.url) if center.logo else '',
                'courses': list(center_courses),
            })

        courses = Course.objects.filter(
            Q(name__icontains=query) | 
            Q(level__name__icontains=query)
        ).select_related('edu_center', 'level').prefetch_related('days')

        for course in courses:
            courses_data.append({
                'name': course.name,
                'level_name': course.level.name,
                'edu_center_logo': request.build_absolute_uri(course.edu_center.logo.url) if course.edu_center.logo else '',
                'edu_center_name': course.edu_center.name,
                'days': '-'.join([day.name[:2] for day in course.days.all()]),
            })
    
    return JsonResponse({
        'centers': centers_data,
        'courses': courses_data
    })
    

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
    

class CourseView(ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['edu_centers'] = EduCenter.objects.all()

        context['events'] = Events.objects.all()

        return context
    

def search_courses(request):
    query = request.GET.get('q', '')
    courses = Course.objects.filter(name__icontains=query)  
    course_data = []

    for course in courses:
        course_data.append({
            'name': course.name,
            'edu_center_logo': request.build_absolute_uri(course.edu_center.logo.url),
            'level_name': course.level.name,
            'days': ', '.join([day.name for day in course.days.all()]),
            'days_html': ''.join([f'<div class="course-item-day">{day.name}</div>' for day in course.days.all()]),
            'intensive_html': '<div class="course-item-day intensive">Intensiv</div>' if course.intensive else '',
            'start_time': course.start_time.strftime('%H:%M')
        })
    
    return JsonResponse({'courses': course_data})

def filter_courses(request):
    tags = request.GET.getlist('states[]', [])
    starting_cost = request.GET.get('starting_cost')
    ending_cost = request.GET.get('ending_cost')
    teacher_gender = request.GET.getlist('teacher_gender')
    selected_days = request.GET.getlist('days')

 
    courses = Course.objects.all()
    if tags:
        courses = courses.filter(categories__name__in=tags)
    if starting_cost and ending_cost:
        courses = courses.filter(price__gte=starting_cost, price__lte=ending_cost)
    if teacher_gender:
        courses = courses.filter(teacher__gender__in=teacher_gender)
    if selected_days:
        courses = courses.filter(days__name__in=selected_days).distinct()

    course_data = []
    for course in courses:
        course_data.append({
            'name': course.name,
            'edu_center_logo': request.build_absolute_uri(course.edu_center.logo.url),
            'level_name': course.level.name,
            'days': ', '.join([day.name for day in course.days.all()]),
            'days_html': ''.join([f'<div class="course-item-day">{day.name}</div>' for day in course.days.all()]),
            'intensive_html': '<div class="course-item-day intensive">Intensiv</div>' if course.intensive else '',
            'start_time': course.start_time.strftime('%H:%M')
        })
    
    return JsonResponse({'courses': course_data})
    

class CompaniesView(ListView):
    model = EduCenter
    template_name = 'companies.html'
    context_object_name = 'edu_centers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['events'] = Events.objects.all()

        return context
    
