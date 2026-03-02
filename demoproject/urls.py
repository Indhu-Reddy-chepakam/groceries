"""
URL configuration for demoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
   # path('home/', views.home, name='home'),
    #path('index/', views.index, name='index'),
    #path('login/', views.login_view, name='login'),
    #path('vegetables/', views.vegetables, name='vegetables'),
    #path('fruits/' ,views.fruits, name='fruits'),
    #path('cart/', views.cart,name='cart'),
    path('', include('myapp.urls')),   # ✅ only include app urls


    
]
