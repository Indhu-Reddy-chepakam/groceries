from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('profile/', views.profile, name='profile'),

    path('vegetables/', views.vegetables, name='vegetables'),
    path('fruits/', views.fruits, name='fruits'),
    path('groceries/', views.groceries, name='groceries'),
    path('stationery/', views.stationery, name='stationery'),
    path('essentials/', views.essentials, name='essentials'),
    path('decor/', views.decor, name='decor'),

    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:index>/', views.remove_from_cart, name='remove_from_cart'),

    path('contact/', views.contact, name='contact'),
]