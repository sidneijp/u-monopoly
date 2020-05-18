"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

import apps.core.urls


schema_view = get_schema_view(
    openapi.Info(
        title="DuAgro API",
        default_version='v1',
        description="Default Application API",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dev@duagro.com.br"),
        license=openapi.License(name="New BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

swagger_urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apps.core.urls)),
    path('api/auth/', include('rest_framework.urls')),
    path('api/swagger/', include(swagger_urlpatterns)),
    path('queue/', include('django_rq.urls')),
]
