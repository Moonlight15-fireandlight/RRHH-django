from django.urls import path
from main import views

urlpatterns = [
    #path('login/', views.login, name='login'),
    path('registerpage/', views.registerpage, name='register'),
    path('loginpage/', views.loginpage, name='loginpage'),
    #path('', views.home, name='home'), #hacer un redirect a home
    path('home/<str:username>/', views.home, name='home'),
    #path('events/<event_id>', views.events, name='events'),
    path('renovacion/', views.renovacion, name='renovar'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('contratos/', views.contratos, name='contratos'),
    path('comisiones', views.comisiones, name='comisiones'),
    path('renovaciones/', views.renovaciones, name='total renovaciones'),
    path('actualizar/<event_id>', views.actualizar, name='actualizarrenovacion'),
    path('actualizarrrhh/<event_id>', views.actualizarrrhh, name='actualizarporrrhh'),
    #path('delete_event/<event_id>', views.delete_event, name='delete_event'),
    path('constancias', views.constancias, name='constancias'),
]
 #https://stackoverflow.com/questions/3209906/django-return-redirect-with-parameters