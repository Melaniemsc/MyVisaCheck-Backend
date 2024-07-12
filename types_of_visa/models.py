from django.db import models

class Visa(models.Model):
  def __str__(self):
    return f'{self.type}'

  type = models.CharField(max_length=80, unique=True)