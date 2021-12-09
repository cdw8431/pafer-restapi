from django.urls import path

from users.views import UserSignInAPIView, UserSignUpAPIView

app_name = 'users'

urlpatterns = [
    path('signup', UserSignUpAPIView.as_view(), name="signup"),
    path('signin', UserSignInAPIView.as_view(), name="signin")
]