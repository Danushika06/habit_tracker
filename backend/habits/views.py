from rest_framework import generics
from .models import Habit
from .serializers import HabitSerializer


class HabitListCreateView(generics.ListCreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
