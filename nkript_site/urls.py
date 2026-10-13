from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/<int:project_id>/", views.project_detail, name="project_detail"),
    path("packages/", views.packages, name="packages"),
    path("quote/<int:package_id>/", views.quote_request, name="quote_request"),
    path("quote/success/", views.quote_success, name="quote_success"),
    path("contact/", views.contact, name="contact"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
