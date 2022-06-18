"""djangoProject3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
import testApp.views as t_a_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', t_a_views.main_page),
    path('login', t_a_views.login_users),
    path('user_admin', t_a_views.login_users),
    path('item/<str:item_id>/', t_a_views.item),
    path('category/<str:category_name>/<int:page_num>', t_a_views.category),
    path('basket', t_a_views.basket),
    path('search/<int:page_num>', t_a_views.search),
    path('complete_purchase/', t_a_views.complete_purchase),
    path('logout', t_a_views.logout_users),


]
