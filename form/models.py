from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator

MATERIAL_CHOICES=(
    ('Lumber', 'LUMBER'),
    ('Steel','STEEL'),
    ('Shingles','SHINGLES'),
    ('Nails','NAILS')
)
# Create your models here.
class MaterialsModel(models.Model):
    manager_name = models.CharField(max_length=40)
    materials_used = models.CharField(max_length=10, choices=MATERIAL_CHOICES)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    time_submitted = models.DateTimeField(default=datetime.now)
    date_submitted = models.DateField(default=datetime.today)

    class Meta:
        ordering = ('-time_submitted',)

    def __str__(self):
        return "Name: " + self.manager_name + ", Material type: " + self.materials_used + ", Quantity: " + str(self.quantity) + ", Time: " +  str(self.time_submitted) 


class ClockInModel(models.Model):
    employee_name = models.CharField(max_length=40)
    time_arrived = models.DateTimeField(default=datetime.now)
    date_submitted = models.DateField(default=datetime.today)

    class Meta:
        unique_together = (('employee_name','date_submitted'),)
        ordering = ('date_submitted',)


class ClockOutModel(models.Model):
    employee_name = models.CharField(max_length=40)
    time_departed = models.DateTimeField(default=datetime.now)
    date_submitted = models.DateField(default=datetime.today)

    class Meta:
        unique_together = (('employee_name','date_submitted'),)
        ordering = ('-date_submitted',) 