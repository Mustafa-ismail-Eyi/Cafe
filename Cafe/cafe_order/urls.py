from distutils.sysconfig import customize_compiler
from django.urls import path 
from . import views

app_name = 'cafe_order'
urlpatterns = [
    path('', views.welcome,name='root'),
    path('register/', views.customer_register,name='register'),
    path('login/', views.customer_login, name='login'),
    path('home/', views.customer_home, name='home'),
    path('logout/', views.customer_logout, name = 'logout'),
    path('create_order/<str:id>/', views.create_order, name="create_order"),
    path('list_orders/', views.list_orders, name = "list_orders"),
    path('delete_food/<str:id>/',views.delete_food, name = "delete_food"),
    path('confirm_order/<str:id>/', views.confirm_order, name = 'confirm_order'),
    path('confirmed_order/', views.confirmed_order, name = 'confirmed_order'),
    path('list_confirmed_orders/', views.list_confirmed_orders, name='list_confirmed_orders')
]