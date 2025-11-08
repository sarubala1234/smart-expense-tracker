from django.db import models

# Create your models here.
class  smart(models.Model):
    title  = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    amount  = models.FloatField()
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.title} - ${self.amount}"
