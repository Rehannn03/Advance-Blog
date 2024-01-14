"""
URL configuration for advanceblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

# for static and media files
from django.conf import settings
from django.conf.urls.static import static


from blog.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('showprofiles',show_all_profiles,name='showprofiles'),
    path('showprofile/<int:id>',show_profile,name='show_profile'),
    path('add_blog',add_blog,name='add_blog'),
    path('show_categories',show_categories,name='show_categories'),
    path('show_blog/<int:id>',show_blog,name='show_blog'),




    path('login',login_user,name='login_user'),
    path('home',home,name='home'),


]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)