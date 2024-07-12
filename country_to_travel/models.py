from django.db import models
from types_of_visa.models import Visa

# Create your models here.
class CountryToTravel(models.Model):
  def __str__(self):
    return f'{self.country_from} to {self.country_to}'
  country_from = models.ForeignKey(
    'countries.country', 
    on_delete=models.CASCADE, 
    related_name='countries_from')
  country_to = models.ForeignKey(
    'countries.country', 
    on_delete=models.CASCADE, 
    related_name='countries_to')
  visa_type = models.ManyToManyField(
    Visa,
    related_name= 'visa',
    blank=True,
  )
  allowed_stay = models.CharField(max_length=300, blank=True)
  notes = models.TextField(max_length=300)

  class Meta:
    unique_together = ('country_from', 'country_to',)

