from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("chat.urls")),
    path('auth/', include("users.urls")),
    path('admin/', admin.site.urls),
    path('api/', include("api.urls"))
]

# Asinngs the custom view to handler404
handler404 = 'hermes.views.custom_404'
