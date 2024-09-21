from django.db import models

from django.core.validators import RegexValidator
# Create your models here.
from django.contrib.auth.models import User


class Level(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    levels = models.ManyToManyField(Level)
    icon_class = models.CharField(max_length=255, null=True, default='fa-regular fa-sparkles', help_text="Font Awesome icon class, e.g., 'fa-calculator-simple'")

    def __str__(self):
        return self.name


class Day(models.Model):
    name = models.CharField(max_length=10, unique=True) 

    def __str__(self):
        return self.name

class EducationType(models.Model):
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class EduCenter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=200)
    description = models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '911234567'. Up to 12 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    edu_type = models.ForeignKey(EducationType, on_delete=models.CASCADE, null=True)
    logo = models.ImageField(upload_to='logos/')
    categories = models.ManyToManyField('Category', blank=True, related_name='edu_centers')
    verify = models.BooleanField(default=False)
    partner = models.BooleanField(default=False)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    instagram_link = models.CharField(max_length=300, blank=True)
    telegram_link = models.CharField(max_length=300, blank=True)
    facebook_link = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name
    

class Branch(models.Model):
    name = models.CharField(max_length=255)
    edu_center = models.ForeignKey(EduCenter, on_delete=models.CASCADE)
    location = models.CharField(max_length=300)
    
    

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    edu_center = models.ForeignKey(EduCenter, related_name='courses', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    days = models.ManyToManyField(Day)
    start_date = models.DateTimeField()
    now_place = models.IntegerField()
    current_place = models.IntegerField()
    teacher = models.CharField(max_length=255)
    price = models.IntegerField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    start_time = models.TimeField()  
    ending_time = models.TimeField()
    intensive = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.edu_center.categories.add(self.category)


class Events(models.Model):
    name = models.CharField(max_length=255)
    banner = models.ImageField(upload_to='events')
    edu_center = models.ForeignKey(EduCenter, on_delete=models.CASCADE)
    day = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name