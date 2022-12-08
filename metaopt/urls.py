from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

handler404 = 'metaopt.views.custom_page_not_found'
handler500 = 'metaopt.views.custom_server_error'
handler403 = 'metaopt.views.custom_permission_denied'
handler400 = 'metaopt.views.custom_bad_request'