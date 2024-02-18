from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_framework.routers import DefaultRouter
from app.recipes.views import RecipeViewSet
from app.chat.views import admin_chat_view

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)

urlpatterns = [path('admin/chat/', admin_chat_view, name='admin_chat'),
               path('admin/', admin.site.urls),
               path('api/v1/', include(router.urls)),
               path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
               path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),
                   ] + urlpatterns
