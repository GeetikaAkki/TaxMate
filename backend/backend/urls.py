from django.urls import path
from .views import create_user, update_user, get_all_users, delete_user

urlpatterns = [
    path('api/users/create/', create_user, name='create_user'),
    path('api/users/update/<int:user_id>/', update_user, name='update_user'),
    path('api/users/all/', get_all_users, name='get_all_users'),
    path('api/users/delete/<int:user_id>/', delete_user, name='delete_user'),
]
