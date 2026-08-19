from django.urls import path
from .views import HabitListCreateView

urlpatterns = [
    path('habits/', HabitListCreateView.as_view(), name='habit-list-create'),
]
