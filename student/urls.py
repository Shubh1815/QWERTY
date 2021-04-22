from django.urls import path
from .views import dashboard, profile, calorie_tracker, expense_tracker, tracker, get_student_data

app_name = 'student'

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('profile/', profile, name="profile"),
    path('tracker/calorie/', calorie_tracker, name="calorie_tracker"),
    path('tracker/expense/', expense_tracker, name="expense_tracker"),
    path('tracker/<str:option>/<int:days>/', tracker, name="tracker_data"),
    path('<str:enrollment_no>/', get_student_data, name="get_student_data"),
]
