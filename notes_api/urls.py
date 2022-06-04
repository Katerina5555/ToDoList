"""to_do_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from notes_api import views

urlpatterns = [
    path('notes/', views.ListNoteAPIView.as_view()),
    path('note/<int:pk>', views.OneNoteAPIView.as_view()),
    path('allnotes/', views.ListNoteAPIView.as_view()),
    path('public/', views.PublicNotesListAPIView.as_view()),
    path('filterau/', views.NotesListCreateAPIView.as_view()),

]
