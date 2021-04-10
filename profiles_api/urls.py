from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles_api import views

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('createnote/', views.CreateNoteForDay.as_view()),
    path('registration/', views.CreateUserProfile.as_view()),
    path('notelist/', views.NoteListForUser.as_view()),
]
