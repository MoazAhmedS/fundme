from django.db import models
from django.shortcuts import get_object_or_404
# Create your models here.
from accounts.models import ProfileUser

class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name="Category Name")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name="Project Title")
    details = models.CharField(max_length=200, verbose_name="Project Details")
    target = models.IntegerField(verbose_name="Project Target")
    current_donations = models.IntegerField(verbose_name="Current Donations")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    create_date = models.DateField(auto_now_add=True, verbose_name="Create Date")
    status = models.BooleanField(default=False, verbose_name="Project Status")
    featured = models.BooleanField(default=False, verbose_name="Is Featured")
    userObject = models.ForeignKey(to=ProfileUser,on_delete=models.CASCADE)
    categoryObject = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    @classmethod 
    def getProjById(cls,id):
        return get_object_or_404(cls,id=id)

    
class Images(models.Model):
    projectObject = models.ForeignKey(Project, on_delete=models.CASCADE,)
    path = models.ImageField(upload_to='project/imgs/')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
