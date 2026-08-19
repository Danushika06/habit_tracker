from django.db import models


class Habit(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    completed_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['habit', 'completed_date'], name='unique_habit_completed_date')
        ]

    def __str__(self):
        return f"{self.habit.name} - {self.completed_date}"
