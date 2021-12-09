from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token,
                                      verify_jwt_token)

api_urls = [
    path('users/', include('users.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth', obtain_jwt_token),
    path('api-token-verify', verify_jwt_token),
    path('api-token-refresh', refresh_jwt_token),
    path('api/', include(api_urls))
]
