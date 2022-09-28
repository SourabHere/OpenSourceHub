from django.urls import path, include
from . import views

urlpatterns = [
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerUser,name="register"),

    path('', views.profiles , name="profiles"),
    path('profile/<str:pk>', views.userProfiles , name="user-profile"),
    path('account/',views.UserAcccount,name='account'),
    
    path('edit_account/',views.editAccount,name="edit_account"),
]