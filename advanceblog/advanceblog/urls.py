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
    path('follow_user',follow_user,name='follow_user'),
    path('showprofile/<int:id>',show_profile,name='show_profile'),



    path('add_blog',add_blog,name='add_blog'),
    path('show_categories',show_categories,name='show_categories'),
    path('show_blog/<int:id>',show_blog,name='show_blog'),
    path('like_blog',like_blog,name='like_blog'),
    path('add_comment',add_comment,name='add_comment'),

    path('add_to_draft',add_to_draft,name='add_to_draft'),
    path('view_draft',view_draft,name='view_draft'),
    path('publish_draft',publish_draft,name='publish_draft'),
    path('remove_draft',remove_draft,name='remove_draft'),



    path('add_to_favourite',add_to_favourite,name='add_to_favourite'),
    path('remove_from_favourite',remove_from_favourite,name='remove_from_favourite'),
    path('get_favourites',get_favourites,name='get_favourites'),


    path('category/<str:cat_name>',show_blogs_based_on_category,name='catgory_blog'),




    path('login',login_user,name='login_user'),
    path('register_user',register_user,name='register_user'),
    path('home',home,name='home'),


]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)