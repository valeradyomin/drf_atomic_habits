from django.urls import path
from habits.apps import HabitsConfig
from habits.views import CreateHabitsAPIView, ListHabitsAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/create/', CreateHabitsAPIView.as_view(), name='create'),
    path('habits/list/', ListHabitsAPIView.as_view(), name='list'),
]
