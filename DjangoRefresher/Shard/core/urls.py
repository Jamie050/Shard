from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name="register"),
    path('logout',views.logoutUser,name="logout"),
    path('login',views.loginUser,name="login"),

    path('edit-post/<str:pk>',views.editPost,name="edit-post"),
    path('delete-post/<str:pk>',views.deletePost,name="delete-post"),

    path('profile/<str:pk>',views.profilePage,name="profile"),
    path('edit-profile/<str:pk>',views.editProfile,name="edit-profile"),

    path('post-comments/<str:pk>',views.commentSection,name="post-comments"),

    path('follow/<str:pk>',views.follow,name="follow"),
    path('unfollow/<str:pk>',views.unfollow,name="unfollow"),
]
