from django.urls import path
from . import views

urlpatterns = [
    # Internal endpoints
    path('chat/', views.chat_api, name='chat_api'),
    
    # No config endpoint
    path('default/', views.default_api, name='default_api'),

    # TusListasWeb endpoints
    path('tlw/', views.tlw_api, name='tlw_api'),
    
    # Porfolio endpoints
    path('porfolio/', views.porfolio_api, name='porfolio_api'),
        
    # Dellpinos.com
    path('dellpinos/', views.dellpinos_api, name='dellpinos_api'),
    
    # Stuff&Scripts endpoints
    path('stuff/', views.stuff_api, name='stuff_api'),
]