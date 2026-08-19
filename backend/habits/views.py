from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Habit, HabitLog
from .serializers import HabitSerializer


class HabitListCreateView(generics.ListCreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitDeleteView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitToggleView(APIView):
    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk)
        completed_date = request.data.get('date', date.today())

        existing_log = HabitLog.objects.filter(
            habit=habit, completed_date=completed_date
        ).first()

        if existing_log:
            existing_log.delete()
            return Response({'checked': False})

        HabitLog.objects.create(habit=habit, completed_date=completed_date)
        return Response({'checked': True})
