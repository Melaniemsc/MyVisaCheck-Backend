from django.urls import path
from .views import CountrylistView, CountryDetailView, CountryVisaRequirement, CountrysSeed

urlpatterns = [
  path('', CountrylistView.as_view()),
  path('<str:name>/', CountryDetailView.as_view()),
  path('admin/visa_requirements/', CountryVisaRequirement.as_view()),
  path('admin/countries/', CountrysSeed.as_view()),
]

