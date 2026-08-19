from datetime import date, timedelta
from django.db import models


class Habit(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def current_streak(self):
        logged_dates = set(self.logs.values_list('completed_date', flat=True))
        streak = 0
        day = date.today()
        while day in logged_dates:
            streak += 1
            day -= timedelta(days=1)
        return streak

    def completion_rate(self):
        days_tracked = (date.today() - self.created_at.date()).days + 1
        completed_days = self.logs.count()
        return round((completed_days / days_tracked) * 100, 1)


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    completed_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['habit', 'completed_date'], name='unique_habit_completed_date')
        ]

    def __str__(self):
        return f"{self.habit.name} - {self.completed_date}"
