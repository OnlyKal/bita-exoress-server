import django.urls
from django.urls import path, include
from menu.views import SignInView, SignupView, UpdatePasswordView, UpdateUserInfoView, UploadAvatarView


urlpatterns = [
    path('user/signin/', SignInView.as_view(), name='signin'),
    path('user/signup/', SignupView.as_view(), name='signup'),
    path('user/update/', UpdateUserInfoView.as_view(), name='update-user'),
    path('user/password/', UpdatePasswordView.as_view(), name='update-password'),
    path('user/avatar/', UploadAvatarView.as_view(), name='update-avatar'),
]

