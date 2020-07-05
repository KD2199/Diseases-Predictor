from django.db import models
from django.contrib.auth.models import User


class Report_Data(models.Model):
    Patient_Name = models.CharField(max_length=50)
    Patient_Id=models.CharField(max_length=50,default='')
    Email = models.EmailField(max_length=50)
    Mobile_No = models.CharField(max_length=50)
    Age = models.CharField(max_length=300)
    mean_radius=models.CharField(max_length=50)
    mean_texture=models.CharField(max_length=50)
    mean_perimeter=models.CharField(max_length=50)
    mean_area=models.CharField(max_length=50)
    mean_smoothness=models.CharField(max_length=50)
    Test_Result=models.CharField(max_length=50)

    def __str__(self):
        return self.Patient_Name
