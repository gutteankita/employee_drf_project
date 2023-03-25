from django.urls import path
from Emp_App import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('employee/', views.EmployeeApiView.as_view()),

    
]