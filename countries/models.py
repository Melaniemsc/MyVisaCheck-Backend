from django.db import models

# Create your models here.
class Country(models.Model):
  def __str__(self):
    return f'{self.name}'
  name = models.CharField(max_length=200)
  nationality = models.CharField(max_length=80)
  flag = models.CharField(max_length=300, blank=True)


