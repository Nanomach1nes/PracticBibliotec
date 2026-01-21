from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API всех приложений
    path('api/', include('apps.authors.urls')),
    path('api/', include('apps.publishers.urls')),
    path('api/', include('apps.genres.urls')),
    path('api/', include('apps.books.urls')),
    path('api/', include('apps.readers.urls')),
    path('api/', include('apps.loans.urls')),
    path('api/', include('apps.reservations.urls')),
    path('api/', include('apps.fines.urls')),
    path('api/', include('apps.librarians.urls')),
    path('api/reports/', include('apps.reports.urls')),

    # Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]