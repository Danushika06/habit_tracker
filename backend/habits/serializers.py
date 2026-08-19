from rest_framework import serializers
from .models import Habit, HabitLog


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['id', 'completed_date']


class HabitSerializer(serializers.ModelSerializer):
    logs = HabitLogSerializer(many=True, read_only=True)
    current_streak = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = ['id', 'name', 'category', 'created_at', 'logs', 'current_streak', 'completion_rate']

    def get_current_streak(self, obj):
        return obj.current_streak()

    def get_completion_rate(self, obj):
        return obj.completion_rate()
