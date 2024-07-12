from django.urls import path
from .views import RegisterView, LoginView, UserSummaryView

urlpatterns = [
path('register/', RegisterView.as_view()),
path('login/', LoginView.as_view()),
path('summary/', UserSummaryView.as_view()),

]