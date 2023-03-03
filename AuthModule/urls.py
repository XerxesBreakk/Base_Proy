from django.urls import path
from .views import UserListView,UserUpdateView,UserCreateView

urlpatterns = [
    path('users/',UserListView.as_view(),name='user_listview'),
    path('update_user/<int:id>',UserUpdateView.as_view(),name='user_updateview'),
    path('delete_user/<int:id>',UserUpdateView.as_view(),name='user_deleteview'),
    path('create_user/',UserCreateView.as_view(),name='user_createview'),
]
