"""FileSharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.forms.widgets import static
from django.urls import path
from note.views import * 
from setuptools.extern import names 
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/',about,name='about'),
    path('',index,name='index'), 
    path('contact/', contact,name='contact'),
    path('login/', userlogin,name = 'login'),
    path('adminlogin/', adminlogin,name = 'adminlogin'), 
    path('signup/', signup1,name = 'signup'),
    path('adminhome/', adminhome,name = 'adminhome'),
    path('logout/', Logout,name = 'logout'),
    path('profile/', Profile,name = 'user_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('changepassword/', changepassword, name = 'change_password'), 
    path('uploadnote/', upload_note, name='uploadnote'), 
    path('view_mynotes/', view_mynotes, name='view_mynotes'),
    path('delete_mynote/<int:pid>/', delete_mynote, name='delete_mynote'),
    path('viewuser/', viewuser, name='view_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('pending/', pending, name='pending'),
    path('accepted/', accepted, name='accepted'), 
    path('rejected/', rejected, name='rejected'),
    path('all_notes/', all_notes, name='all_notes'),
    path('asign_status/<int:pid>/', asign_status, name='asign_status'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
