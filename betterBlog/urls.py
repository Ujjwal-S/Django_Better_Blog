from django.contrib import admin
from django.urls import path, include
from accounts import git_update_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
	path('', include('blog.urls')),
	path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('update_server/', git_update_view.update, name='production-update'),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  