from django.urls import path

from users import views
from django.conf.urls import url

app_name = 'users'
username_regex = r'[a-zA-Z0-9_]+'

handler404 = '{app_name}.views.handler404'.format(app_name=app_name)
handler500 = '{app_name}.views.handler500'.format(app_name=app_name)

urlpatterns = [
    path('users/register/', views.signup, name='register'),
    path('users/profile/<int:pk>', views.UserProfile.as_view(), name='user-profile'),
    path('users/login/', views.user_login, name='login'),
    path('users/logout/', views.logout_view, name='logout'),
    path('users/profile/<int:pk>/edit/', views.EditUserProfileView.as_view(), name="edit-user-profile"),
]

