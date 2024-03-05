from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitsPagination
from habits.serializers import HabitsSerializer


class CreateHabitsAPIView(generics.CreateAPIView):
    serializer_class = HabitsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListHabitsAPIView(generics.ListAPIView):
    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitsPagination
    permission_classes = [IsAuthenticated]
