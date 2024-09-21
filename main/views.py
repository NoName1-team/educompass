from django.shortcuts import render

from django.http import JsonResponse
from django.views.generic import ListView
from django.db.models import Count, Q
from .models import EduCenter, Course, Category, Events, Day, Teacher




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
        context['categories'] = Category.objects.all()
        context['days'] = Day.objects.all()
        context['teachers'] = Teacher.objects.all()

        # Add the current GET parameters to context to preserve form inputs
        context['selected_categories'] = self.request.GET.getlist('categories')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['selected_gender'] = self.request.GET.get('gender', '')
        context['selected_days'] = self.request.GET.getlist('days')

        return context

    def get_queryset(self):
        queryset = Course.objects.all()
        categories = self.request.GET.getlist('categories')
        min_price = self.request.GET.get('min_price', 0)
        max_price = self.request.GET.get('max_price', 1000000)
        gender = self.request.GET.get('gender', None)
        days = self.request.GET.getlist('days')
        if categories:
            queryset = queryset.filter(category__id__in=categories)

        # Step 2: Filter by Price
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        # Step 3: Filter by Teacher Gender
        if gender:
            queryset = queryset.filter(teacher__gender__iexact=gender)
        if days:
            queryset = queryset.filter(days__name__in=days)
        queryset = queryset.distinct()

        return queryset


    
def search_courses(request):
    query = request.GET.get('q', '')
    courses = Course.objects.filter(
        Q(name__icontains=query) | 
        Q(level__name__icontains=query) | 
        Q(days__name__icontains=query)
    ).select_related('edu_center', 'level').prefetch_related('days').distinct()

    results = []
    for course in courses:
        days_html = ''.join([f'<div class="course-item-day">{day.name}</div>' for day in course.days.all()])
        
        results.append({
            'name': course.name,
            'edu_center_logo': course.edu_center.logo.url if course.edu_center.logo else '',
            'level_name': course.level.name,
            'days_html': days_html,  
            'start_time': course.start_time.strftime("%H:%M"),
            'intensive_html': '<div class="course-item-day intensive">Intensive <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f525/512.webp" alt=""/></div>' if course.intensive else '',
        })

    return JsonResponse({'courses': results})


class CompaniesView(ListView):
    model = EduCenter
    template_name = 'companies.html'
    context_object_name = 'edu_centers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['events'] = Events.objects.all()

        return context
    
