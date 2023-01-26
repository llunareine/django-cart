from django.urls import path

from . import views

urlpatterns = [
    path('users', views.Users.as_view(), name='users'),
    path('users/<int:user_id>', views.UserDetail.as_view(), name='user_id')
]