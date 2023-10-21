# Third-party imports
from baton.autodiscover import admin
from rest_framework import urls, routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Django imports
from django.urls import path, re_path, include

# Application imports
from t_link import views
from django.urls import path, re_path, include
from rest_framework import urls, routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from missionlink.views import *

# Set up schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="T-link API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.t-link.com/terms/",
        contact=openapi.Contact(email="contact@t-link.com"),
        license=openapi.License(name="T-link License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # 이 아랫 부분은 우리가 사용하는 app들의 URL들을 넣습니다.
    # path('app이름', include('app이름.urls'))
    path("api-", include("t_link.urls")),
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
