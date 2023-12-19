from django.urls import path
from . import views

urlpatterns = [
    #path('login/', views.login, name='login'),
    #path('', views.lobby, name='lobby'),
    path('', views.login, name='login'),
    path('lobby/', views.lobby, name='lobby'),
    path('room/', views.room),
    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
    path('get_user_locations/', views.get_user_locations)
]