from django.db import models
from accounts.models import ProfileUser
from project.models import Project

class Donation(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} donated {self.amount} to {self.project.name}"
