from django.urls import path
from .views import HabitListCreateView, HabitDeleteView, HabitToggleView

urlpatterns = [
    path('habits/', HabitListCreateView.as_view(), name='habit-list-create'),
    path('habits/<int:pk>/', HabitDeleteView.as_view(), name='habit-delete'),
    path('habits/<int:pk>/toggle/', HabitToggleView.as_view(), name='habit-toggle'),
]
