from django.db import models
from accounts.models import ProfileUser  
from project.models import Project       
from django.core.validators import MinValueValidator, MaxValueValidator

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tag Name",unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class ProjectTag(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Project")
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Tag")

    class Meta:
        verbose_name = "Project Tag"
        verbose_name_plural = "Project Tags"
        unique_together = ('project_id', 'tag_id') 

    def __str__(self):
        return f"{self.project.title} - {self.tag.name}"


class Rate(models.Model):
    user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Project")
    rate_value = models.PositiveSmallIntegerField(
        verbose_name="Rate Value",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    note = models.TextField(blank=True, null=True, verbose_name="Note")

    class Meta:
        verbose_name = "Rate"
        verbose_name_plural = "Rates"
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.user.username} rated {self.project.title} - {self.rate_value}"
