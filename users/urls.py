from django.urls import path
from django.contrib.auth import views as auth_views

from users import views
from django.conf.urls import url

app_name = 'users'
username_regex = r'[a-zA-Z0-9_]+'

handler404 = '{app_name}.views.handler404'.format(app_name=app_name)
handler500 = '{app_name}.views.handler500'.format(app_name=app_name)

urlpatterns = [
    path('register/', views.signup, name='register'),
    url(r'^profile/(?P<pk>{})/$'.format(username_regex), views.UserProfile.as_view(), name='user-profile'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>/edit/', views.EditUserProfileView.as_view(), name="edit-user-profile"),
]

