from django.urls import path
from .views import CountryToTravelView

urlpatterns = [
  path('', CountryToTravelView.as_view()),
]

